import operator

# TODO: "as" operator


def aggregate_op(expr, context, mode):
    ops_for = [expr[1]] if isinstance(expr[1], str) else eval_expr(expr[1], context)
    op_on = expr[2]
    data = eval_expr(expr[3], context)
    result = {}
    counts = {}

    for d in data:
        key = tuple(d[op_for] for op_for in ops_for)

        if mode in {"sum", "avg", "max", "min"} and not isinstance(
            d[op_on], (float, int)
        ):
            raise Exception(f"{op_on} must be numeric for use in {mode} function")

        val = d.get(op_on, 1)

        if mode == "max":
            result[key] = max(result.get(key, val - 1), val)
        elif mode == "min":
            result[key] = min(result.get(key, val + 1), val)
        elif mode in {"sum", "avg"}:
            result[key] = result.get(key, 0) + val
            counts[key] = counts.get(key, 0) + 1
        elif mode == "count":
            result[key] = result.get(key, 0) + 1
        else:
            raise Exception(f"Unknown mode: {mode}")

    if mode == "avg":
        for key in result:
            result[key] /= counts[key]

    return [
        {
            **{op_for: k for op_for, k in zip(ops_for, key)},
            (op_on if mode != "count" else "count"): val,
        }
        for key, val in result.items()
    ]


def count_op(expr, context):
    dummy_expr = expr[:2] + [""] + [expr[2]]
    return aggregate_op(dummy_expr, context, "count")


def make_aggregate_op(mode):
    return lambda expr, context: aggregate_op(expr, context, mode)


def list_op(expr, context):
    if not isinstance(context, dict):
        raise Exception("ERROR: filter expects a dict. instead got: \n" + str(context))
    members = context.keys() if expr[1] == "*" else expr[1:]
    return {str(m): eval_expr(m, context) for m in members}


def map_op(expr, context):
    data = eval_expr(expr[1], context)
    if not isinstance(data, list):
        raise Exception("map expects a list. instead got: \n" + str(data))
    format = expr[2]
    formatted = [eval_expr(format, row) for row in data]
    return [f for f in formatted if f is not None]


def make_order_op(type):
    def order_op(expr, context):
        order_by = (
            [expr[1]] if isinstance(expr[1], str) else eval_expr(expr[1], context)
        )
        data = eval_expr(expr[2], context)

        reverse = type == "desc"

        try:
            data.sort(key=lambda x: tuple(x.get(k) for k in order_by), reverse=reverse)
            return data
        except Exception as e:
            raise Exception(f"ERROR: failed to order by {order_by} ({type}): {e}")

    return order_op


def filter_op(expr, context):
    cond = expr[1]
    data = eval_expr(expr[2], context)
    return [row for row in data if eval_expr(cond, row)]


def join_op(expr, context):
    join_cond = expr[1]
    left_data = eval_expr(expr[2], context)
    right_data = eval_expr(expr[3], context)
    joined = []
    for left in left_data:
        for right in right_data:
            if any(key in right for key in left):
                clash_keys = [key for key in left if key in right]
                raise Exception(f"ERROR: clashing keys! {', '.join(clash_keys)}")
            merged = {**left, **right}
            if eval_expr(join_cond, merged):
                joined.append(merged)

    return joined


def limit_op(expr, context):
    limit = None
    try:
        limit = int(float(eval_expr(expr[1], context)))
    except:
        raise Exception(f"ERROR: failed to parse limiter {limit}")
    data = eval_expr(expr[2], context)
    return data[:limit]


def make_binary_op(operation, return_type="str"):
    def binary_op(expr, context):
        left = float(eval_expr(expr[1], context))
        right = float(eval_expr(expr[2], context))
        result = operation(left, right)
        return str(result) if return_type == "str" else result

    return binary_op


def and_op(expr, context):
    expressions = expr[1:]
    return all(eval_expr(e, context) for e in expressions)


def or_op(expr, context):
    expressions = expr[1:]
    return any(eval_expr(e, context) for e in expressions)


def equals_op(expr, context):
    return str(eval_expr(expr[1], context)) == str(eval_expr(expr[2], context))


def not_equals_op(expr, context):
    return not equals_op(expr, context)


def get_op(expr, context):
    source = context[expr[1]]
    if not source:
        raise KeyError("data source not found: " + expr[1])
    if len(expr) > 2:
        return eval_expr(expr[2], source)
    return source


op_funs = {
    # sub-queries
    "get": {"op": get_op, "arg_range": 1},
    "list": {"op": list_op, "arg_range": [1, float("inf")]},
    "map": {"op": map_op, "arg_range": 2},
    "join": {"op": join_op, "arg_range": 3},
    "limit": {"op": limit_op, "arg_range": 2},
    "ascending": {"op": make_order_op("asc"), "arg_range": 2},
    "descending": {"op": make_order_op("desc"), "arg_range": 2},
    # formatters
    "filter": {"op": filter_op, "arg_range": 2},
    # aggregators
    "count": {"op": count_op, "arg_range": 2},
    "sum": {"op": make_aggregate_op("sum"), "arg_range": 3},
    "max": {"op": make_aggregate_op("max"), "arg_range": 3},
    "min": {"op": make_aggregate_op("min"), "arg_range": 3},
    "avg": {"op": make_aggregate_op("avg"), "arg_range": 3},
    # pure operators
    "==": {"op": equals_op, "arg_range": 2},
    "!=": {"op": not_equals_op, "arg_range": 2},
    "and": {"op": and_op, "arg_range": [2, float("inf")]},
    "or": {"op": or_op, "arg_range": [2, float("inf")]},
    "+": {"op": make_binary_op(operator.add, "str"), "arg_range": 2},
    "-": {"op": make_binary_op(operator.sub, "str"), "arg_range": 2},
    "*": {"op": make_binary_op(operator.mul, "str"), "arg_range": 2},
    "/": {"op": make_binary_op(operator.truediv, "str"), "arg_range": 2},
    "//": {"op": make_binary_op(operator.floordiv, "str"), "arg_range": 2},
    "**": {"op": make_binary_op(operator.pow, "str"), "arg_range": 2},
    "<": {"op": make_binary_op(operator.lt, "bool"), "arg_range": 2},
    ">": {"op": make_binary_op(operator.gt, "bool"), "arg_range": 2},
    ">=": {"op": make_binary_op(operator.ge, "bool"), "arg_range": 2},
    "<=": {"op": make_binary_op(operator.le, "bool"), "arg_range": 2},
}


# Evaluator
def eval_expr(expr, context={}):
    if isinstance(expr, str):
        return context.get(expr, expr)

    op = expr[0]
    op_info = op_funs.get(op, False)
    if not op_info:
        raise Exception("operator not found: '" + op + "'")

    arg_range = op_info["arg_range"]
    n_args = len(expr[1:])

    if isinstance(arg_range, int):
        if n_args != arg_range:
            raise Exception(
                f"ERROR: {op} accepts exactly {arg_range} arguments. Received {n_args}"
            )
    else:
        min_args, max_args = arg_range
        if not (min_args <= n_args <= max_args):
            raise Exception(
                f"ERROR: {op} accepts between {min_args} and {max_args} arguments. Received {n_args}"
            )

    return op_info["op"](expr, context)

import operator

# TODO: "as" operator

def validate_keys(row, required_keys):
    missing = [k for k in required_keys if k not in row]
    if missing:
        raise Exception(f"Missing key(s) {missing} in record: {row}")
    return True


def validate_types(method, obj, types):
    if not isinstance(obj, types):
        raise Exception(f"ERROR: {method} expects [{types}]. instead got: {obj}\n")


def resolve_ids(raw, context):
    return {raw: raw} if isinstance(raw, str) else eval_expr(raw, context)


def compute_aggregate(val, current, mode):
    if mode == "max":
        return val if current is None else max(current, val)
    elif mode == "min":
        return val if current is None else min(current, val)
    elif mode in {"sum", "avg"}:
        return (current or 0) + val
    elif mode == "count":
        return (current or 0) + 1
    raise Exception(f"Unknown mode: {mode}")


def aggregate_op(expr, context, mode):
    group_ids = resolve_ids(expr[1], context)
    aggregate_ids = resolve_ids(expr[2], context)
    data = eval_expr(expr[3], context)

    result = {}
    counts = {} if mode == "avg" else None
    numeric_modes = {"sum", "avg", "max", "min"}

    for d in data:
        validate_keys(d, set(group_ids) | set(aggregate_ids))
        key = tuple(d[k] for k in group_ids)
        result.setdefault(key, {})
        if mode == "avg":
            counts.setdefault(key, {})

        for source, alias in aggregate_ids.items():
            val = d[source]
            if mode in numeric_modes:
                validate_types(mode, val, (int, float))

            current = result[key].get(alias)
            result[key][alias] = compute_aggregate(val, current, mode)

            if mode == "avg":
                counts[key][alias] = counts[key].get(alias, 0) + 1

    output = []
    for key, values in result.items():
        if mode == "avg":
            for alias in values:
                values[alias] /= counts[key][alias]
        row = {alias: key[i] for i, alias in enumerate(group_ids.values())}
        row.update(values)
        output.append(row)

    return output


def count_op(expr, context):
    dummy_expr = [expr[0], expr[1], "", expr[2]]
    return aggregate_op(dummy_expr, context, "count")


def make_aggregate_op(mode):
    return lambda expr, context: aggregate_op(expr, context, mode)


def list_op(expr, context):
    validate_types("list", context, (dict))
    context_keys = context.keys() if expr[1] == "*" else expr[1:]
    return {str(k): eval_expr(k, context) for k in context_keys}


def map_op(expr, context):
    data = eval_expr(expr[1], context)
    validate_types("map", data, (list))

    format_expr = expr[2]
    required_keys = set(format_expr[1:])

    output = []
    for row in data:
        validate_keys(row, required_keys)
        result = eval_expr(format_expr, row)
        if result is not None:
            output.append(result)

    return output


def make_order_op(type):
    def order_op(expr, context):
        order_by = (
            [expr[1]] if isinstance(expr[1], str) else eval_expr(expr[1], context)
        )
        data = eval_expr(expr[2], context)

        reverse = type == "desc"

        for row in data:
            validate_keys(row, order_by)

        try:
            data.sort(key=lambda x: tuple(x[k] for k in order_by), reverse=reverse)
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

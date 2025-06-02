import operator
import sys


def aggregate_op(expr, context, mode):
    op_for = expr[1]
    op_on = expr[2]
    data = eval_expr(expr[3], context)
    result = {}

    for d in data:
        if not isinstance(d[op_on], (float, int)):
            print(f"{op_on} must be numeric for use in {mode} function")
            sys.exit(1)

        if mode == "max":
            result[d[op_for]] = max(result.get(d[op_for], d[op_on] - 1), d[op_on])
        elif mode == "min":
            result[d[op_for]] = min(result.get(d[op_for], d[op_on] + 1), d[op_on])
        elif mode == "sum":
            result[d[op_for]] = result.get(d[op_for], 0) + d[op_on]
        else:
            print(f"Unknown mode: {mode}")
            sys.exit(1)

    return [{op_for: key, op_on: value} for key, value in result.items()]


def make_aggregate_op(mode):
    return lambda expr, context: aggregate_op(expr, context, mode)


def list_op(expr, context):
    if not isinstance(context, dict):
        print("ERROR: filter expects a dict. instead got: \n" + str(context))
        sys.exit(1)
    keys = context.keys() if expr[1] == "*" else expr[1:]
    return {e: eval_expr(e, context) for e in keys}


def map_op(expr, context):
    sub_query = expr[1]
    data = eval_expr(sub_query, context)
    if not isinstance(data, list):
        print("map expects a list. instead got: \n" + str(data))
        sys.exit(1)
    cond = expr[2]
    matches = [eval_expr(cond, row) for row in data]
    return [m for m in matches if m is not None]


def if_op(expr, context):
    cond = eval_expr(expr[1], context)
    if cond:
        return eval_expr(expr[2], context)
    elif len(expr) > 3:
        return eval_expr(expr[3], context)
    return None


def join_op(expr, context):
    join_cond = expr[1]
    left_data = eval_expr(expr[2], context)
    right_data = eval_expr(expr[3], context)
    joined = []
    for left in left_data:
        for right in right_data:
            if any(key in right for key in left):
                clash_keys = [key for key in left if key in right]
                print(f"ERROR: clashing keys! {', '.join(clash_keys)}")
                sys.exit(1)
            merged = {**left, **right}
            if eval_expr(join_cond, merged):
                joined.append(merged)

    return joined


def make_math_op(operation):
    def math_op(expr, context):
        left = float(eval_expr(expr[1], context))
        right = float(eval_expr(expr[2], context))
        return str(operation(left, right))

    return math_op


def make_bool_op(operation):
    def bool_op(expr, context):
        left = float(eval_expr(expr[1], context))
        right = float(eval_expr(expr[2], context))
        return operation(left, right)

    return bool_op


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
    "get": {"op": get_op, "arg_range": 1},
    "list": {"op": list_op, "arg_range": [1, float('inf')]},
    "map": {"op": map_op, "arg_range": 2},
    "join": {"op": join_op, "arg_range": 3},
    "sum": {"op": make_aggregate_op("sum"), "arg_range": 3},
    "max": {"op": make_aggregate_op("max"), "arg_range": 3},
    "min": {"op": make_aggregate_op("min"), "arg_range": 3},
    "==": {"op": equals_op, "arg_range": 2},
    "!=": {"op": not_equals_op, "arg_range": 2},
    "if": {"op": if_op, "arg_range": [2, 3]},
    "+": {"op": make_math_op(operator.add), "arg_range": 2},
    "-": {"op": make_math_op(operator.sub), "arg_range": 2},
    "*": {"op":  make_math_op(operator.mul), "arg_range": 2},
    "/": {"op": make_math_op(operator.truediv), "arg_range": 2},
    "//": {"op": make_math_op(operator.floordiv), "arg_range": 2},
    "**": {"op": make_math_op(operator.pow), "arg_range": 2},
    "<": {"op": make_bool_op(operator.lt), "arg_range": 2},
    ">": {"op": make_bool_op(operator.gt), "arg_range": 2},
    ">=": {"op": make_bool_op(operator.ge), "arg_range": 2},
    "<=": {"op": make_bool_op(operator.le), "arg_range": 2},
    "and": {"op": and_op, "arg_range": [2, float('inf')]},
    "or": {"op": or_op, "arg_range": [2, float('inf')]},
}


# Evaluator
def eval_expr(expr, context={}):
    if isinstance(expr, str):
        return context.get(expr, expr)

    op = expr[0]
    op_info = op_funs.get(op, False)
    if not op_info:
        print("operator not found: '" + op + "'")
        sys.exit(1)
    
    arg_range = op_info["arg_range"]
    n_args = len(expr[1:])

    if isinstance(arg_range, int):
        if n_args != arg_range:
            print(f"ERROR: {op} accepts exactly {arg_range} arguments. Received {n_args}")
            sys.exit(1)
    else:
        min_args, max_args = arg_range
        if not (min_args <= n_args <= max_args):
            print(f"ERROR: {op} accepts between {min_args} and {max_args} arguments. Received {n_args}")
            sys.exit(1)

    return op_info["op"](expr, context)

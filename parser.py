# Parser that builds a nested list
def parse(tokens):
    if not tokens:
        raise SyntaxError("Unexpected EOF")
    token = tokens.pop(0)
    if token == "(":
        L = []
        while tokens[0] != ")":
            L.append(parse(tokens))
        tokens.pop(0)  # pop ')'
        return L
    elif token == ")":
        raise SyntaxError("Unexpected )")
    else:
        return token

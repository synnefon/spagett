from tables import data_sources
from parser import parse
from tokenizer import tokenize
from printer import print_table
from evaluator import eval_expr


# Load .🍝 file
def load_spagett_file(filename):
    if not filename.endswith(".🍝"):
        print("ERROR: only able to process .🍝 files at this time")
    with open(filename, "r") as f:
        return f.read()


# Main runner
def run_spagett(filename):
    code = load_spagett_file(filename)
    tokens = tokenize(code)
    ast = parse(tokens)
    result = eval_expr(ast, data_sources)
    print_table(result)


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python spagett.py <file.🍝>")
    else:
        run_spagett(sys.argv[1])

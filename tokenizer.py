import re


# Basic tokenizer
def tokenize(code):
    code = re.sub(r"\s+", " ", code.strip())
    tokens = re.findall(r"\(|\)|[^\s()]+", code)
    return tokens

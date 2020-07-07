from collections import OrderedDict

operations = OrderedDict([
    ("+", lambda x, y: x + y),
    ("-", lambda x, y: x - y),
    ("/", lambda x, y: x / y),
    ("*", lambda x, y: x * y),
    ("^", lambda x, y: x ^ y)
])
    
symbols = operations.keys()

def lex(expr):
    tokens = []
    while expr:
        char, *expr = expr
        if char == "(":
            try:
                paren, expr = lex(expr)
                tokens.append(paren)
            except ValueError:
                raise Exception("paren mismatch")
        elif char == ")":
            return tokens, expr
        elif char.isdigit() or char == ".":
            try:
                if tokens[-1] in symbols:
                    tokens.append(char)
                elif type(tokens[-1]) is list:
                    raise Exception("parens cannot be followed by numbers")
                else:
                    tokens[-1] += char
            except IndexError:
                tokens.append(char)
        elif char in symbols:
            tokens.append(char)
        elif char.isspace():
            pass
        else:
            raise Exception("invalid character: " + char)
    return tokens

def evaluate(tokens):
    for symbol, func in operations.items():
        try:
            pos = tokens.index(symbol)
            leftTerm = evaluate(tokens[:pos])
            rightTerm = evaluate(tokens[pos + 1:])
            return func(leftTerm, rightTerm)
        except ValueError:
            pass
    if len(tokens) == 1:
        try:
            return float(tokens[0])
        except TypeError:
            return evaluate(tokens[0])
    else:
        raise Exception("bad expression: " + tokens)

def calc(expr):
    return evaluate(lex(expr))
    
while 1:
    print(calc(input("Input? ")))
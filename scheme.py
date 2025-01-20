from interpreter import SchemeInterpreter
from antlr4 import FileStream, CommonTokenStream
import sys
from schemeLexer import schemeLexer
from schemeParser import schemeParser


def main():
    # Para tratar las ejecuciones erróneas
    if len(sys.argv) != 2:
        print("Uso: python3 scheme.py archivo.scm")
        sys.exit(1)

    input_file = sys.argv[1]
    input_stream = FileStream(input_file, encoding="utf-8")
    lexer = schemeLexer(input_stream)
    token_stream = CommonTokenStream(lexer)
    parser = schemeParser(token_stream)
    tree = parser.root()

    interpreter = SchemeInterpreter()
    results = interpreter.visit(tree)


if __name__ == "__main__":
    main()

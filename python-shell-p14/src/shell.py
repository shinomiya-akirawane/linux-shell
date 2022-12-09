from antlr4 import InputStream, CommonTokenStream
import sys
import os

from parserTree.CommandLexer import CommandLexer
from parserTree.CommandParser import CommandParser
from parserTreeVisitor import parserTreeVisitor


def shell(cmdline):
    lexer = CommandLexer(InputStream(cmdline))
    stream = CommonTokenStream(lexer)
    parser = CommandParser(stream)
    tree = parser.command()
    cmd = tree.accept(parserTreeVisitor())
    cmd.eval()


if __name__ == "__main__":
    args_num = len(sys.argv) - 1
    if args_num > 0:
        if args_num != 2:
            raise ValueError("wrong number of command line arguments")
        if sys.argv[1] != "-c":
            raise ValueError(f"unexpected command line argument {sys.argv[1]}")
        shell(sys.argv[2])

    else:
        while True:
            print(os.getcwd() + "> ", end="")
            cmdline = input()
            if cmdline.strip() == "":
                pass
            else:
                shell(cmdline)

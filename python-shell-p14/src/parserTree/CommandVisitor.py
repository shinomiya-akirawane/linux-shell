# Generated from Command.g4 by ANTLR 4.11.1
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .CommandParser import CommandParser
else:
    from CommandParser import CommandParser

# This class defines a complete generic visitor for a parse tree produced by CommandParser.

class CommandVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by CommandParser#command.
    def visitCommand(self, ctx:CommandParser.CommandContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CommandParser#partialSeq.
    def visitPartialSeq(self, ctx:CommandParser.PartialSeqContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CommandParser#prefixCall.
    def visitPrefixCall(self, ctx:CommandParser.PrefixCallContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CommandParser#partialPipe.
    def visitPartialPipe(self, ctx:CommandParser.PartialPipeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CommandParser#call.
    def visitCall(self, ctx:CommandParser.CallContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CommandParser#atom.
    def visitAtom(self, ctx:CommandParser.AtomContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CommandParser#argument.
    def visitArgument(self, ctx:CommandParser.ArgumentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CommandParser#redirection.
    def visitRedirection(self, ctx:CommandParser.RedirectionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CommandParser#quoted.
    def visitQuoted(self, ctx:CommandParser.QuotedContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CommandParser#unquoted.
    def visitUnquoted(self, ctx:CommandParser.UnquotedContext):
        return self.visitChildren(ctx)



del CommandParser
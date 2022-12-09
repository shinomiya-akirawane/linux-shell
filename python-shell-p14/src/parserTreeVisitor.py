from typing import Union, TextIO
from io import StringIO
from os import getcwd
from re import findall
from antlr4 import InputStream, CommonTokenStream
import sys

from parserTree.CommandVisitor import CommandVisitor
from parserTree.CommandParser import CommandParser
from parserTree.CommandLexer import CommandLexer

from command import Call, Seq, Command, Pipe
from apps.commandStream import CommandStream


class parserTreeVisitor(CommandVisitor):
    def visitCommand(self, ctx: CommandParser.CommandContext) -> Seq:
        # check if there is any perfixCall node or partialSeq node below
        prefixCallCtx = ctx.prefixCall()
        partialSeqCtx = ctx.partialSeq()

        prefixCall = self.visitPrefixCall(prefixCallCtx)
        if partialSeqCtx:
            prefixCall = Seq(prefixCall)
            self.visitPartialSeq(partialSeqCtx, prefixCall)
        return prefixCall

    def visitPartialSeq(
        self, ctx: CommandParser.PartialSeqContext, partialSeq: Seq
    ):
        prefixCallCtx = ctx.prefixCall()
        partialSeqCtx = ctx.partialSeq()

        prefixCall = self.visitPrefixCall(prefixCallCtx)
        partialSeq.addCommand(prefixCall)
        if partialSeqCtx:
            self.visitPartialSeq(partialSeqCtx, partialSeq)

    def visitPrefixCall(self, ctx: CommandParser.PrefixCallContext):
        callCtx = ctx.call()
        partialPipeCtx = ctx.partialPipe()

        cmd = self.visitCall(callCtx)
        if partialPipeCtx:
            cmd = self.visitPartialPipe(partialPipeCtx, cmd)
        return cmd

    def visitPartialPipe(
        self, ctx: CommandParser.PartialPipeContext, call: Command
    ) -> Pipe:
        pipe = Pipe(
            call,
            self.visitCall(ctx.call()),
            CommandStream(getcwd(), stdout=sys.stdout, args=["pwd"]),
        )
        partialPipeCtx = ctx.partialPipe()

        if partialPipeCtx:
            return self.visitPartialPipe(partialPipeCtx, pipe)
        else:
            return pipe

    def visitCall(
        self, ctx: CommandParser.CallContext
    ) -> Union[Call, Command]:
        argumentsContext = ctx.argument()
        arguments = self.visitArgument(argumentsContext)
        redirectionCtx = ctx.redirection()
        atomCtx = ctx.atom()
        stdin = None
        stdout = sys.stdout
        if redirectionCtx:
            for elem in redirectionCtx:
                stdin, stdout = self.visitRedirection(elem, stdin, stdout)

        if atomCtx:
            for elem in atomCtx:
                atom = self.visitAtom(elem, stdin, stdout)
                # if the node below the elem node is argument node
                if elem.argument():
                    arguments.extend(atom)
                # if the node below the elem node is redirection node
                else:
                    stdin, stdout = atom

        return Call(CommandStream(getcwd(), stdin, stdout, arguments))

    def visitRedirection(
        self,
        ctx: CommandParser.RedirectionContext,
        stdin: TextIO,
        stdout: TextIO
    ) -> TextIO:
        sign = ctx.getChild(0).getText()
        if sign == "<":
            stdin = open(getcwd() + "/" + ctx.argument().getText(), "r")
        elif sign == ">":
            stdout = open(getcwd() + "/" + ctx.argument().getText(), "w")
        return stdin, stdout

    def visitArgument(self, ctx: CommandParser.ArgumentContext) -> list:
        argument = ""
        for elem in ctx.getChildren():
            if type(elem).__name__ == "QuotedContext":
                argument += self.visitQuoted(elem)
            else:
                argument += elem.getText()
        return argument.split(' ')

    def visitAtom(
        self, ctx: CommandParser.AtomContext, stdin: TextIO, stdout: TextIO
    ) -> Union[list, TextIO]:
        # if there is redirection below the passed node
        if ctx.redirection() is not None:
            stdin, stdout = self.visitRedirection(
                            ctx.redirection(), stdin, stdout
                            )
            return stdin, stdout
        else:
            arguments = self.visitArgument(ctx.argument())
            return arguments

    def visitQuoted(self, ctx: CommandParser.QuotedContext) -> str:

        # deal with substitution command in the backQuotes
        def subCmdEval(cmd):
            lexer = CommandLexer(InputStream(cmd))
            stream = CommonTokenStream(lexer)
            parser = CommandParser(stream)
            tree = parser.command()
            subcmd = tree.accept(parserTreeVisitor())
            # tempStdout is used to store the result of sequence subcmd
            tempStdout = StringIO()
            if type(subcmd) == Seq:
                for command in subcmd.commands:
                    command.commandStream.setStdout(tempStdout)
            else:
                subcmd.commandStream.setStdout(tempStdout)
            subcmd.eval()
            return tempStdout.getvalue()

        if ctx.SINGLE_QUOTED():
            content = str(ctx.SINGLE_QUOTED()).replace("'", "")
            return content

        # substitution command
        elif ctx.BACKQUOTED():
            cmd = str(ctx.BACKQUOTED()).replace("`", "")
            newArgs = subCmdEval(cmd)
            newArgs = newArgs.replace("\n", " ")
            newArgs = newArgs.strip()
            return newArgs

        # doubleQuoted arguments may including substition
        else:
            doublequoted = str(ctx.DOUBLE_QUOTED()).replace('"', "")
            matches = findall("`[^`]*`", doublequoted)
            if matches != []:
                for match in matches:
                    match_cmd = match[1:-1]
                    newArgs = subCmdEval(match_cmd)
                    doublequoted = doublequoted.replace(match, newArgs, 1)
            return doublequoted

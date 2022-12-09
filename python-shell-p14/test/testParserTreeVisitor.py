import unittest
from os import mkdir, getcwd, remove, rmdir
from sys import stdout
from src.command import Call
from antlr4 import InputStream, CommonTokenStream
from src.apps.commandStream import CommandStream
from src.parserTree.CommandLexer import CommandLexer
from src.parserTree.CommandParser import CommandParser
from src.parserTreeVisitor import parserTreeVisitor


class TestParserTreeVisitor(unittest.TestCase):
    @classmethod
    def setUpClass(self) -> None:
        mkdir("folder1")
        self.cwd = getcwd()
        with open("folder1/a.txt", "w") as f:
            f.write("aaa")
        with open("folder1/b.txt", "w") as f:
            f.write("")

    @classmethod
    def tearDownClass(self) -> None:
        remove("folder1/a.txt")
        remove("folder1/b.txt")
        rmdir("folder1")

    def assertCallContent(self, command: Call, expectStream: CommandStream):
        self.assertEqual(type(command).__name__, "Call")
        self.assertEqual(
            type(command.app).__name__.lower(),
            expectStream.getAppName().lower()
        )
        self.assertEqual(command.commandStream, expectStream)

    def parseCommand(self, cmd):
        lexer = CommandLexer(InputStream(cmd))
        stream = CommonTokenStream(lexer)
        parser = CommandParser(stream)
        tree = parser.command()
        return tree.accept(parserTreeVisitor())

    def testBasicCallCommand(self):
        parserTree = self.parseCommand("echo aaa bbb")
        self.assertCallContent(
            parserTree,
            CommandStream(
                getcwd(),
                None,
                stdout,
                ["echo", "aaa", "bbb"]
                )
        )

    def testDoubleQuotedArgs(self):
        parseTree = self.parseCommand('echo "hello world"')
        self.assertCallContent(
            parseTree,
            CommandStream(
                getcwd(),
                None,
                stdout,
                ["echo", "hello world"]
                )
        )

    def testSingleQuotedArgs(self):
        parseTree = self.parseCommand("echo 'hello world'")
        self.assertCallContent(
            parseTree,
            CommandStream(
                getcwd(),
                None,
                stdout,
                ["echo", "hello world"]
                )
        )

    def testSequenceCommand(self):
        parseTree = self.parseCommand("cd folder1 ; cat a.txt")
        self.assertEqual(type(parseTree).__name__, "Seq")
        self.assertEqual(len(parseTree.commands), 2)
        self.assertCallContent(
            parseTree.commands[0],
            CommandStream(
                getcwd(),
                None,
                stdout,
                ["cd", "folder1"]
                )
        )
        self.assertCallContent(
            parseTree.commands[1],
            CommandStream(
                getcwd(),
                None,
                stdout,
                args=["cat", "a.txt"],
            )
        )

    def testPipeCommand(self):
        parseTree = self.parseCommand("cat folder1/a.txt | sort | uniq")
        self.assertEqual(type(parseTree).__name__, "Pipe")
        self.assertCallContent(
            parseTree.leftCmd.leftCmd,
            CommandStream(
                getcwd(),
                None,
                stdout,
                ["cat", "folder1/a.txt"]
                )
        )
        self.assertCallContent(
            parseTree.leftCmd.rightCmd,
            CommandStream(
                getcwd(),
                None,
                stdout,
                ["sort"]
                )
        )
        self.assertCallContent(
            parseTree.rightCmd,
            CommandStream(
                getcwd(),
                None,
                stdout,
                ["uniq"]
                )
        )

    def testRedirection(self):
        parseTree = self.parseCommand(
            "head -n 2 < folder1/a.txt > folder1/b.txt"
            )
        stdin = open("folder1/a.txt", "w")
        reStdout = open("folder1/b.txt", "w")
        self.assertCallContent(
            parseTree,
            CommandStream(
                getcwd(),
                stdin,
                reStdout,
                args=["head", "-n", "2"])
        )

    def testRedirectionInfront(self):
        parseTree = self.parseCommand("< folder1/a.txt cat")
        stdin = open("folder1/a.txt", "r")
        self.assertCallContent(
            parseTree,
            CommandStream(
                getcwd(),
                stdin,
                stdout,
                ["cat"]
                )
        )

    def testSubstitution(self):
        parseTree = self.parseCommand(("echo `echo abc`"))
        self.assertCallContent(
            parseTree,
            CommandStream(
                getcwd(),
                None,
                stdout,
                ["echo", "abc"]
                )
        )

    def testSubstitutionSequence(self):
        parseTree = self.parseCommand("echo `echo foo; echo bar`")
        self.assertCallContent(
            parseTree,
            CommandStream(
                getcwd(),
                None,
                stdout,
                ["echo", "foo", "bar"]
                )
        )

    def testDoublequotedSubstitution(self):
        parseTree = self.parseCommand('echo "`echo abc`"')
        self.assertCallContent(
            parseTree,
            CommandStream(
                getcwd(),
                None,
                stdout,
                ["echo", "abc\n"]
                )
        )

    def testNestedDoublequotes(self):
        parseTree = self.parseCommand('echo "a `echo "b"`"')
        self.assertCallContent(
            parseTree,
            CommandStream(
                getcwd(),
                None,
                stdout,
                ["echo", "a b\n"]
                )
        )


if __name__ == "__main__":
    unittest.main()

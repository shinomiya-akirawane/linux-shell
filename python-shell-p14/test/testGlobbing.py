import unittest
from os import getcwd, mkdir, chdir, remove, rmdir
from io import StringIO
from src.apps.cat import Cat
from src.apps.echo import Echo
from src.apps.grep import Grep
from src.apps.commandStream import CommandStream


class testGlobbing(unittest.TestCase):
    def setUp(self) -> None:
        self.cwd = getcwd()
        self.cat = Cat()
        self.echo = Echo()
        self.grep = Grep()
        self.result = StringIO()
        self.pathOrignial = getcwd()
        mkdir('dirGlobbing')
        chdir('dirGlobbing')
        self.path = getcwd()
        with open("GlobbingA.txt", "w") as f:
            f.write("AAA\nABB\nCCC\n")
        with open("GlobbingB.txt", "w") as f:
            f.write("ADD\nAEE\nFFF\n")
        with open("GlobbingC.txt", "w") as f:
            f.write("AGG\nAHH\nIII\n")

    def tearDown(self) -> None:
        remove("GlobbingA.txt")
        remove("GlobbingB.txt")
        remove("GlobbingC.txt")
        chdir(self.pathOrignial)
        rmdir(self.path)

    def testglobbingCat(self):
        catCommand = CommandStream(
            getcwd(),
            None,
            self.result,
            ["cat", "*.txt"]
            )
        self.cat.exec(catCommand)
        stdout = catCommand.getStdout().getvalue()
        self.assertEqual(
            stdout,
            "AAA\nABB\nCCC\nADD\nAEE\nFFF\nAGG\nAHH\nIII\n"
            )

    def testglobbingEcho(self):
        echoCommand = CommandStream(
            getcwd(),
            None,
            self.result,
            ["echo", "*.txt"]
            )
        self.echo.exec(echoCommand)
        stdout = echoCommand.getStdout().getvalue()
        self.assertEqual(
            stdout,
            "GlobbingA.txt\nGlobbingB.txt\nGlobbingC.txt\n"
            )

    def testglobbingGrep(self):
        grepCommand = CommandStream(
            getcwd(),
            None,
            self.result,
            ["grep", "A..", "*.txt"]
        )
        self.grep.exec(grepCommand)
        stdout = grepCommand.getStdout().getvalue()
        self.assertEqual(
            stdout,
            ("GlobbingA.txt:AAA\nGlobbingA.txt:ABB\nGlobbingB.txt:ADD\n"
             "GlobbingB.txt:AEE\nGlobbingC.txt:AGG\nGlobbingC.txt:AHH\n")
        )


if __name__ == "__main__":
    unittest.main()

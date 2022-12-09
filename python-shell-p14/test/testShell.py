import unittest
from src.shell import shell
from io import StringIO
from contextlib import redirect_stdout
import os


class TestShell(unittest.TestCase):

    def setUp(self) -> None:
        with open('PipeFile.txt', "w") as f:
            f.write('BBB\nAAA\nCCC\n')

    def tearDown(self) -> None:
        os.remove('PipeFile.txt')

    def testShellEcho(self):
        out = StringIO()
        with redirect_stdout(out):
            shell("echo hello world")

        output = out.getvalue()
        self.assertEqual(output, "hello world\n")

    def testShellPipe(self):
        out = StringIO()
        with redirect_stdout(out):
            shell("cat PipeFile.txt | sort")

        output = out.getvalue()
        self.assertEqual(output, "AAA\nBBB\nCCC\n")


if __name__ == "__main__":
    unittest.main()

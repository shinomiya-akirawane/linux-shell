import unittest
from os import getcwd
from sys import stdout
from src.apps.commandStream import CommandStream


class TestCommandStream(unittest.TestCase):
    def testPwdWrongNumber(self):
        with self.assertRaises(ValueError):
            CommandStream(
                getcwd(),
                None,
                stdout,
                ['pwd', 'a']
                )

    def testCdWrongNumber(self):
        with self.assertRaises(ValueError):
            CommandStream(
                getcwd(),
                None,
                stdout,
                ['cd']
                )

    def testLsWrongNumber(self):
        with self.assertRaises(ValueError):
            CommandStream(
                getcwd(),
                None,
                stdout,
                ['ls', 'a', 'b']
                )

    def testEchoWrongNumber(self):
        with self.assertRaises(ValueError):
            CommandStream(
                getcwd(),
                None,
                stdout,
                ['echo']
                )

    def testHeadOrTailWrongNumber(self):
        with self.assertRaises(ValueError):
            CommandStream(
                getcwd(),
                None,
                stdout,
                ['head', '-n', '10', '15', 'a.txt']
                )

    def testHeadOrTailWrongOptionWithFile(self):
        with self.assertRaises(ValueError):
            CommandStream(
                getcwd(),
                None,
                stdout,
                ['head', 'n', '15', 'a.txt']
                )

    def testHeadOrTailWrongOption(self):
        with self.assertRaises(ValueError):
            CommandStream(
                getcwd(),
                None,
                stdout,
                ['tail', 'n', '15']
                )

    def testGrepWrongNumber(self):
        with self.assertRaises(ValueError):
            CommandStream(
                getcwd(),
                None,
                stdout,
                ['grep']
                )

    def testCutWrongNumber(self):
        with self.assertRaises(ValueError):
            CommandStream(
                getcwd(),
                None,
                stdout,
                ['cut']
                )

    def testCutWrongOption(self):
        with self.assertRaises(ValueError):
            CommandStream(
                getcwd(),
                None,
                stdout,
                ['cut', 'b', '1', 'a.txt']
                )

    def testFindWrongNumber(self):
        with self.assertRaises(ValueError):
            CommandStream(
                getcwd(),
                None,
                stdout,
                ['find']
                )

    def testFindWrongUsage(self):
        with self.assertRaises(ValueError):
            CommandStream(
                getcwd(),
                None,
                stdout,
                ['find', '*.txt']
                )

    def testUniqOrSortWrongNumber(self):
        with self.assertRaises(ValueError):
            CommandStream(
                getcwd(),
                None,
                stdout,
                ['sort', '-i', '-r', 'a.txt']
                )

    def testUniqOrSortWrongOption(self):
        with self.assertRaises(ValueError):
            CommandStream(
                getcwd(),
                None,
                stdout,
                ['uniq', 'i', 'a.txt']
                )

    def testWcWrongOption(self):
        with self.assertRaises(ValueError):
            CommandStream(
                getcwd(),
                None,
                stdout,
                ['wc', 'l', 'a.txt']
                )

    def testWrongCommand(self):
        with self.assertRaises(ValueError):
            CommandStream(
                getcwd(),
                None,
                stdout,
                ['hello']
                )


if __name__ == "__main__":
    unittest.main()

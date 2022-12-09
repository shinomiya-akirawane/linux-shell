import unittest
from os import getcwd
from sys import stdout
from src.apps.commandStream import CommandStream
from appFactory import AppFactory


class TestUnsafe(unittest.TestCase):
    def testUnsafe(self):
        c = AppFactory.create("_cat")
        cmd = CommandStream(
            getcwd(),
            None,
            stdout,
            ["_cat", "a.txt"]
            )
        error = c.exec(cmd)
        self.assertEqual(str(error), "no such file or directory: a.txt")

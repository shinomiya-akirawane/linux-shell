import unittest
import sys
from os import remove, mkdir, chdir, rmdir, getcwd
from io import StringIO
from src.apps.cat import Cat
from src.apps.cd import Cd
from src.apps.cut import Cut
from src.apps.echo import Echo
from src.apps.find import Find
from src.apps.grep import Grep
from src.apps.head import Head
from src.apps.ls import Ls
from src.apps.myPwd import Pwd
from src.apps.sort import Sort
from src.apps.tail import Tail
from src.apps.uniq import Uniq
from src.apps.wc import Wc

from src.apps.commandStream import CommandStream


class TestCat(unittest.TestCase):
    def setUp(self) -> None:
        self.cat = Cat()
        self.result = StringIO()
        with open("CatFile.txt", "w") as f:
            f.write("AAA\nBBB\nCCC")
        with open("CatStdin.txt", "w") as f:
            f.write("DDD\nEEE\nFFF\n")

    def tearDown(self) -> None:
        remove("CatFile.txt")
        remove("CatStdin.txt")

    def testCat(self):
        cmd = CommandStream(
            getcwd(),
            None,
            self.result,
            ["cat", "CatFile.txt"]
            )
        self.cat.exec(cmd)
        stdout = cmd.getStdout().getvalue()
        self.assertEqual(stdout, "AAA\nBBB\nCCC\n")

    def testCatStdin(self):
        stdin = open("CatStdin.txt", "r")
        cmd = CommandStream(
            getcwd(),
            stdin,
            self.result,
            ["cat"]
            )
        self.cat.exec(cmd)
        stdout = cmd.getStdout().getvalue()
        stdin.close()
        self.assertEqual(stdout, "DDD\nEEE\nFFF\n")

    def testCatStringStdin(self):
        stdin = StringIO('ABC\nabc\n')
        cmd = CommandStream(
            getcwd(),
            stdin,
            self.result,
            ["cat"]
            )
        self.cat.exec(cmd)
        stdout = cmd.getStdout().getvalue()
        self.assertEqual(stdout, 'ABC\nabc\n')

    def testCatException(self):
        cmd = CommandStream(
            getcwd(),
            None,
            self.result,
            ["cat", "file1.txt"]
            )
        with self.assertRaises(FileNotFoundError):
            self.cat.exec(cmd)

    def testCatMissingStdin(self):
        cmd = CommandStream(
            getcwd(),
            None,
            self.result,
            ["cat"]
            )
        with self.assertRaises(ValueError):
            self.cat.exec(cmd)


class TestCd(unittest.TestCase):
    def setUp(self) -> None:
        mkdir("CdDir")
        self.cwd = getcwd()
        self.cd = Cd()

    def tearDown(self) -> None:
        chdir(self.cwd)
        rmdir("CdDir")

    def testCd(self):
        cmd = CommandStream(
            getcwd(),
            None,
            sys.stdout,
            ["cd", "CdDir"]
            )
        self.cd.exec(cmd)
        currDir = cmd.getCurrDir()
        chdir(self.cwd)
        chdir("CdDir")
        self.assertEqual(currDir, getcwd())

    def testCdException(self):
        cmd = CommandStream(
            getcwd(),
            None,
            sys.stdout,
            ["cd", "dir0"]
            )
        with self.assertRaises(FileNotFoundError):
            self.cd.exec(cmd)


class TestCut(unittest.TestCase):
    def setUp(self) -> None:
        self.cut = Cut()
        self.result = StringIO()
        with open("CutFile.txt", "w") as f:
            f.write("ABC\nabc\nXYZ\n")
        with open("CutStdin.txt", "w") as f:
            f.write("DDD\nEEE\nFFF\n")

    def tearDown(self) -> None:
        remove("CutFile.txt")
        remove("CutStdin.txt")

    def testCutNum(self):
        cmd = CommandStream(
            getcwd(),
            None,
            self.result,
            ["cut", "-b", "1,2", "CutFile.txt"]
        )
        self.cut.exec(cmd)
        stdout = cmd.getStdout().getvalue()
        self.assertEqual(stdout, "AB\nab\nXY\n")

    def testCutRangeBack(self):
        cmd = CommandStream(
            getcwd(),
            None,
            self.result,
            ["cut", "-b", "2-", "CutFile.txt"]
        )
        self.cut.exec(cmd)
        stdout = cmd.getStdout().getvalue()
        self.assertEqual(stdout, "BC\nbc\nYZ\n")

    def testCutRangeFront(self):
        cmd = CommandStream(
            getcwd(),
            None,
            self.result,
            ["cut", "-b", "-2", "CutFile.txt"]
        )
        self.cut.exec(cmd)
        stdout = cmd.getStdout().getvalue()
        self.assertEqual(stdout, "AB\nab\nXY\n")

    def testCutRangeMiddle(self):
        cmd = CommandStream(
            getcwd(),
            None,
            self.result,
            ["cut", "-b", "2-4", "CutFile.txt"]
        )
        self.cut.exec(cmd)
        stdout = cmd.getStdout().getvalue()
        self.assertEqual(stdout, "BC\nbc\nYZ\n")

    def testCutStdin(self):
        stdin = open("CutStdin.txt", "r")
        cmd = CommandStream(
            getcwd(),
            stdin,
            self.result,
            ["cut", "-b", "1"])
        self.cut.exec(cmd)
        stdout = cmd.getStdout().getvalue()
        self.assertEqual(stdout, "D\nE\nF\n")

    def testCutByteRangeWithSpace(self):
        cmd = CommandStream(
            getcwd(),
            None,
            self.result,
            ["cut", "-b", "1, 2"])
        with self.assertRaises(ValueError):
            self.cut.exec(cmd)

    def testCutInvalidOption(self):
        cmd = CommandStream(
            getcwd(),
            None,
            self.result,
            ["cut", "-n", "1", "CutFile.txt"]
        )
        with self.assertRaises(ValueError):
            self.cut.exec(cmd)

    def testCutInvalidRange(self):
        cmd = CommandStream(
            getcwd(),
            None,
            self.result,
            ["cut", "-b", "a-b", "CutFile.txt"]
        )
        with self.assertRaises(ValueError):
            self.cut.exec(cmd)

    def testCutMissingStdin(self):
        cmd = CommandStream(
            getcwd(),
            None,
            self.result,
            ["cut", "-b", "1"]
            )
        with self.assertRaises(ValueError):
            self.cut.exec(cmd)

    def testCutNoNumber(self):
        cmd = CommandStream(
            getcwd(),
            None,
            self.result,
            ["cut", "-b", "b", "CutFile.txt"]
        )
        with self.assertRaises(ValueError):
            self.cut.exec(cmd)

    def testCutStringStdin(self):
        stdin = StringIO("abc\nABC\n")
        cmd = CommandStream(
            getcwd(),
            stdin,
            self.result,
            ["cut", "-b", "1"]
            )
        self.cut.exec(cmd)
        stdout = cmd.getStdout().getvalue()
        self.assertEqual(stdout, "a\nA\n")

    def testCutOutOfRange(self):
        cmd = CommandStream(
            getcwd(),
            None,
            self.result,
            ["cut", "-b", "-5", "CutFile.txt"]
        )
        self.cut.exec(cmd)
        stdout = cmd.getStdout().getvalue()
        self.assertEqual(stdout, "ABC\nabc\nXYZ\n")

    def testCutMiddleRange(self):
        cmd = CommandStream(
            getcwd(),
            None,
            self.result,
            ["cut", "-b", "1-2", "CutFile.txt"]
        )
        self.cut.exec(cmd)
        stdout = cmd.getStdout().getvalue()
        self.assertEqual(stdout, "AB\nab\nXY\n")


class TestEcho(unittest.TestCase):
    def setUp(self) -> None:
        self.echo = Echo()
        self.result = StringIO()

    def testEcho(self):
        cmd = CommandStream(
            getcwd(),
            None,
            self.result,
            ["echo", "hello"]
            )
        self.echo.exec(cmd)
        stdout = cmd.getStdout().getvalue()
        self.assertEqual(stdout, "hello\n")


class TestFind(unittest.TestCase):
    def setUp(self) -> None:
        self.find = Find()
        self.result = StringIO()
        self.cwd = getcwd()
        mkdir("FindDirectory")
        chdir("FindDirectory")
        with open("FindFile1.txt", "w") as f:
            f.write("aaa\n")
        with open("FindFile2.txt", "w") as f:
            f.write("bbb\n")
        mkdir("FindSubdirectory")
        with open("FindSubdirectory/FindFile3.txt", "w") as f:
            f.write("ccc\n")

    def tearDown(self) -> None:
        chdir(self.cwd)
        remove("FindDirectory/FindSubdirectory/FindFile3.txt")
        rmdir("FindDirectory/FindSubdirectory")
        remove("FindDirectory/FindFile1.txt")
        remove("FindDirectory/FindFile2.txt")
        rmdir("FindDirectory")

    def testFindCurrentDirectory(self):
        cmd = CommandStream(
            getcwd(),
            None,
            self.result,
            ["find", "-name", "*.txt"]
            )
        self.find.exec(cmd)
        stdout = cmd.getStdout().getvalue()
        self.assertEqual(
            stdout,
            ("./FindFile1.txt\n./FindFile2.txt\n"
             "./FindSubdirectory/FindFile3.txt\n")
        )

    def testFindAnotherDirectory(self):
        cmd = CommandStream(
            getcwd(),
            None,
            self.result,
            ["find", "FindSubdirectory", "-name", "*.txt"]
        )
        self.find.exec(cmd)
        stdout = cmd.getStdout().getvalue()
        self.assertEqual(stdout, "FindSubdirectory/FindFile3.txt\n")

    def testFindNoFile(self):
        cmd = CommandStream(
            getcwd(),
            None,
            self.result,
            ["find", "-name", "A*"])
        with self.assertRaises(FileNotFoundError):
            self.find.exec(cmd)


class TestGrep(unittest.TestCase):
    def setUp(self) -> None:
        self.grep = Grep()
        self.result = StringIO()
        with open("GrepFileA.txt", "w") as f:
            f.write("AAA\nBBB\nACC")
        with open("GrepFileB.txt", "w") as f:
            f.write("ADD\nEEE\nAFF")
        with open("GrepStdin.txt", "w") as f:
            f.write("AGG\nHHH\nAII")

    def tearDown(self) -> None:
        remove("GrepFileA.txt")
        remove("GrepFileB.txt")
        remove("GrepStdin.txt")

    def testGrepSignleFile(self):

        cmd = CommandStream(
            getcwd(),
            None,
            self.result,
            ["grep", "A..", "GrepFileA.txt"]
        )
        self.grep.exec(cmd)
        stdout = cmd.getStdout().getvalue()
        self.assertEqual(stdout, "AAA\nACC\n")

    def testGrepMultiFile(self):
        cmd = CommandStream(
            getcwd(),
            None,
            self.result,
            ["grep", "A..", "GrepFileA.txt", "GrepFileB.txt"],
        )
        self.grep.exec(cmd)
        stdout = cmd.getStdout().getvalue()
        self.assertEqual(
            stdout,
            ("GrepFileA.txt:AAA\nGrepFileA.txt:ACC\n"
             "GrepFileB.txt:ADD\nGrepFileB.txt:AFF\n")
        )

    def testGrepStdin(self):
        stdin = open("GrepStdin.txt", "r")
        cmd = CommandStream(
            getcwd(),
            stdin,
            self.result,
            ["grep", "A.."]
            )
        self.grep.exec(cmd)
        stdout = cmd.getStdout().getvalue()
        stdin.close()
        self.assertEqual(stdout, "AGG\nAII\n")

    def testGrepFileNotFound(self):
        cmd = CommandStream(
            getcwd(),
            None,
            self.result,
            ["grep", "A..", "file1.txt"]
            )
        with self.assertRaises(FileNotFoundError):
            self.grep.exec(cmd)

    def testGrepMultiFileNotFound(self):
        cmd = CommandStream(
            getcwd(),
            None,
            self.result,
            ["grep", "A..", "GrepfileB.txt", "file1.txt"]
        )
        with self.assertRaises(FileNotFoundError):
            self.grep.exec(cmd)

    def testGrepMissingStdin(self):
        cmd = CommandStream(
            getcwd(),
            None,
            self.result,
            ["grep", "A.."]
            )
        with self.assertRaises(ValueError):
            self.grep.exec(cmd)

    def testGrepMissingPattern(self):
        cmd = CommandStream(
            getcwd(),
            None,
            self.result,
            ["grep", "GrepFileA.txt"]
            )
        with self.assertRaises(ValueError):
            self.grep.exec(cmd)

    def testGrepStringStdin(self):
        stdin = StringIO("AAA\nABB\nCCC\n")
        cmd = CommandStream(
            getcwd(),
            stdin,
            self.result,
            ["grep", "A.."]
            )
        self.grep.exec(cmd)
        stdout = cmd.getStdout().getvalue()
        self.assertEqual(stdout, "AAA\nABB\n")


class TestHead(unittest.TestCase):
    def setUp(self) -> None:
        self.head = Head()
        self.result = StringIO()
        with open("HeadFile.txt", "w") as f:
            f.write("A\nB\nC\nD\nE\nF\nG\nH\nI\nJ\nK")
        with open("HeadStdin.txt", "w") as f:
            f.write("A\nB\nC\nD\nE\nF\nG\nH\nI\nJ\nK")

    def tearDown(self) -> None:
        remove("HeadFile.txt")
        remove("HeadStdin.txt")

    def testHeadFile(self):
        headFileCommand = CommandStream(
            getcwd(),
            None,
            self.result,
            ["head", "-n", "7", "HeadFile.txt"]
        )
        self.head.exec(headFileCommand)
        stdout = headFileCommand.getStdout().getvalue()
        self.assertEqual(stdout, "A\nB\nC\nD\nE\nF\nG\n")

    def testHeadFileWithoutOption(self):
        headFileCommand = CommandStream(
            getcwd(),
            None,
            self.result,
            ["head", "HeadFile.txt"]
        )
        self.head.exec(headFileCommand)
        stdout = headFileCommand.getStdout().getvalue()
        self.assertEqual(stdout, "A\nB\nC\nD\nE\nF\nG\nH\nI\nJ\n")

    def testHeadFileLinesLessThenOption(self):
        headFileCommand = CommandStream(
            getcwd(),
            None,
            self.result,
            ["head", "-n", "21", "HeadFile.txt"]
        )
        self.head.exec(headFileCommand)
        stdout = headFileCommand.getStdout().getvalue()
        self.assertEqual(stdout, "A\nB\nC\nD\nE\nF\nG\nH\nI\nJ\nK\n")

    def testHeadStdin(self):
        stdin = open("HeadStdin.txt", "r")
        headStdinCommand = CommandStream(
            getcwd(),
            stdin,
            self.result,
            ["head", "-n", "5"]
        )
        self.head.exec(headStdinCommand)
        stdout = headStdinCommand.getStdout().getvalue()
        self.assertEqual(stdout, "A\nB\nC\nD\nE\n")

    def testHeadStdinWithoutOption(self):
        stdin = open("HeadStdin.txt", "r")
        headStdinCommand = CommandStream(
            getcwd(),
            stdin,
            self.result,
            ["head"]
            )
        self.head.exec(headStdinCommand)
        stdout = headStdinCommand.getStdout().getvalue()
        self.assertEqual(stdout, "A\nB\nC\nD\nE\nF\nG\nH\nI\nJ\n")

    def testHeadStdinLinesLessThenOption(self):
        stdin = open("HeadStdin.txt", "r")
        headStdinCommand = CommandStream(
            getcwd(),
            stdin,
            self.result,
            ["head", "-n", "21"]
        )
        self.head.exec(headStdinCommand)
        stdout = headStdinCommand.getStdout().getvalue()
        self.assertEqual(stdout, "A\nB\nC\nD\nE\nF\nG\nH\nI\nJ\nK\n")

    def testHeadFileNotFound(self):
        command = CommandStream(
            getcwd(),
            None,
            self.result,
            ["head", "-n", "5", "file1.txt"]
        )
        with self.assertRaises(FileNotFoundError):
            self.head.exec(command)

    def testHeadMissingStdin(self):
        command = CommandStream(
            getcwd(),
            None,
            self.result,
            ["head", "-n", "5"]
            )
        with self.assertRaises(ValueError):
            self.head.exec(command)

    def testHeadNoNumberOption(self):
        command = CommandStream(
            getcwd(),
            None,
            self.result,
            ["head", "-n", "b", "HeadFile.txt"]
        )
        with self.assertRaises(ValueError):
            self.head.exec(command)

    def testHeadInvalidOption(self):
        with self.assertRaises(ValueError):
            self.head.exec(
                CommandStream(
                    getcwd(),
                    None,
                    self.result,
                    ["head", "-t", "HeadFile.txt"]
                )
            )

    def testHeadStringStdin(self):
        stdin = StringIO("AAA\nABB\nCCC\n")
        command = CommandStream(
            getcwd(),
            stdin,
            self.result,
            ["head", "-n", "2"]
            )
        self.head.exec(command)
        stdout = command.getStdout().getvalue()
        self.assertEqual(stdout, "AAA\nABB\n")


class TestLs(unittest.TestCase):
    def setUp(self) -> None:
        self.ls = Ls()
        self.result = StringIO()
        self.cwd = getcwd()
        mkdir('LsDirectory')
        chdir('LsDirectory')
        with open('LsFile1.txt', "w") as f:
            f.write('A\n')
        with open('.LsFile2.txt', "w") as f:
            f.write('B\n')
        mkdir('LsSubdirectory')
        with open('LsSubdirectory/LsFile3.txt', "w") as f:
            f.write('C\n')

    def tearDown(self) -> None:
        chdir(self.cwd)
        remove('LsDirectory/LsSubdirectory/LsFile3.txt')
        rmdir('LsDirectory/LsSubdirectory')
        remove('LsDirectory/LsFile1.txt')
        remove('LsDirectory/.LsFile2.txt')
        rmdir('LsDirectory')

    def testLsCurrentDirectory(self):
        cmd = CommandStream(
            getcwd(),
            None,
            self.result,
            ['ls']
            )
        self.ls.exec(cmd)
        stdout = cmd.getStdout().getvalue()
        self.assertEqual(stdout, 'LsFile1.txt\nLsSubdirectory\n')

    def testLsAnotherDirectory(self):
        cmd = CommandStream(
            getcwd(),
            None,
            self.result,
            ['ls', 'LsSubdirectory']
            )
        self.ls.exec(cmd)
        stdout = cmd.getStdout().getvalue()
        self.assertEqual(stdout, 'LsFile3.txt\n')

    def testLsNoDirectory(self):
        cmd = CommandStream(
            getcwd(),
            None,
            self.result,
            ['ls', 'NoDirectory']
            )
        with self.assertRaises(FileNotFoundError):
            self.ls.exec(cmd)


class TestPwd(unittest.TestCase):
    def setUp(self) -> None:
        self.pwd = Pwd()
        result = StringIO()
        self.cmd = CommandStream(
            getcwd(),
            None,
            result,
            ["pwd"]
            )

    def testPwd(self):
        self.pwd.exec(self.cmd)
        stdout = self.cmd.getStdout().getvalue()
        self.assertEqual(stdout, getcwd() + "\n")


class TestSort(unittest.TestCase):
    def setUp(self) -> None:
        self.sort = Sort()
        self.result = StringIO()
        with open("SortFile.txt", "w") as f:
            f.write("A\nC\nB\nE\nD")
        with open("SortStdin.txt", "w") as f:
            f.write("W\nY\nX\nZ\nV\n")

    def tearDown(self) -> None:
        remove("SortFile.txt")
        remove("SortStdin.txt")

    def testSortFile(self):
        cmd = CommandStream(
            getcwd(),
            None,
            self.result,
            ["sort", "SortFile.txt"]
            )
        self.sort.exec(cmd)
        stdout = cmd.getStdout().getvalue()
        self.assertEqual(stdout, "A\nB\nC\nD\nE\n")

    def testSortFileWithReverse(self):
        cmd = CommandStream(
            getcwd(),
            None,
            self.result,
            ["sort", "-r", "SortFile.txt"]
            )
        self.sort.exec(cmd)
        stdout = cmd.getStdout().getvalue()
        self.assertEqual(stdout, "E\nD\nC\nB\nA\n")

    def testSortStdin(self):
        stdin = open("SortStdin.txt", "r")
        cmd = CommandStream(
            getcwd(),
            stdin,
            self.result,
            ["sort"]
            )
        self.sort.exec(cmd)
        stdout = cmd.getStdout().getvalue()
        self.assertEqual(stdout, "V\nW\nX\nY\nZ\n")

    def testSortStdinWithReverse(self):
        stdin = open("SortStdin.txt", "r")
        cmd = CommandStream(
            getcwd(),
            stdin,
            self.result,
            ["sort", "-r"]
            )
        self.sort.exec(cmd)
        stdout = cmd.getStdout().getvalue()
        self.assertEqual(stdout, "Z\nY\nX\nW\nV\n")

    def testSortFileNotFound(self):
        cmd = CommandStream(
            getcwd(),
            None,
            self.result,
            ["sort", "-r", "file1.txt"]
            )
        with self.assertRaises(FileNotFoundError):
            self.sort.exec(cmd)

    def testSortMissingStdin(self):
        cmd = CommandStream(
            getcwd(),
            None,
            self.result,
            ["sort", "-r"]
            )
        with self.assertRaises(ValueError):
            self.sort.exec(cmd)

    def testSortStringStdin(self):
        stdin = StringIO("AAA\nCCC\nBBB")
        cmd = CommandStream(
            getcwd(),
            stdin,
            self.result,
            ["sort"]
            )
        self.sort.exec(cmd)
        stdout = cmd.getStdout().getvalue()
        self.assertEqual(stdout, "AAA\nBBB\nCCC\n")


class TestTail(unittest.TestCase):
    def setUp(self) -> None:
        self.tail = Tail()
        self.result = StringIO()
        with open("TailFile.txt", "w") as f:
            f.write("A\nB\nC\nD\nE\nF\nG\nH\nI\nJ\nK")
        with open("TailStdin.txt", "w") as f:
            f.write("A\nB\nC\nD\nE\nF\nG\nH\nI\nJ\nK")

    def tearDown(self) -> None:
        remove("TailFile.txt")
        remove("TailStdin.txt")

    def testTailFile(self):
        cmd = CommandStream(
            getcwd(),
            None,
            self.result,
            ["tail", "-n", "4", "TailFile.txt"]
        )
        self.tail.exec(cmd)
        stdout = cmd.getStdout().getvalue()
        self.assertEqual(stdout, "H\nI\nJ\nK\n")

    def testTailFileWithoutOption(self):
        cmd = CommandStream(
            getcwd(),
            None,
            self.result,
            ["tail", "TailFile.txt"]
            )
        self.tail.exec(cmd)
        stdout = cmd.getStdout().getvalue()
        self.assertEqual(stdout, "B\nC\nD\nE\nF\nG\nH\nI\nJ\nK\n")

    def testTailFileLinesLessThenOption(self):
        cmd = CommandStream(
            getcwd(),
            None,
            self.result,
            ["tail", "-n", "21", "TailFile.txt"]
        )
        self.tail.exec(cmd)
        stdout = cmd.getStdout().getvalue()
        self.assertEqual(stdout, "A\nB\nC\nD\nE\nF\nG\nH\nI\nJ\nK\n")

    def testTailStdin(self):
        stdin = open("TailStdin.txt", "r")
        cmd = CommandStream(
            getcwd(),
            stdin,
            self.result,
            ["tail", "-n", "5"]
            )
        self.tail.exec(cmd)
        stdout = cmd.getStdout().getvalue()
        self.assertEqual(stdout, "G\nH\nI\nJ\nK\n")

    def testTailStdinWithoutOption(self):
        stdin = open("TailStdin.txt", "r")
        cmd = CommandStream(
            getcwd(),
            stdin,
            self.result,
            ["tail"]
            )
        self.tail.exec(cmd)
        stdout = cmd.getStdout().getvalue()
        self.assertEqual(stdout, "B\nC\nD\nE\nF\nG\nH\nI\nJ\nK\n")

    def testTailStdinLinesLessThenOption(self):
        stdin = open("TailStdin.txt", "r")
        cmd = CommandStream(
            getcwd(),
            stdin,
            self.result,
            ["tail", "-n", "21"]
            )
        self.tail.exec(cmd)
        stdout = cmd.getStdout().getvalue()
        self.assertEqual(stdout, "A\nB\nC\nD\nE\nF\nG\nH\nI\nJ\nK\n")

    def testTailFileNotFound(self):
        cmd = CommandStream(
            getcwd(),
            None,
            self.result,
            ["tail", "-n", "5", "file1.txt"]
        )
        with self.assertRaises(FileNotFoundError):
            self.tail.exec(cmd)

    def testTailMissingStdin(self):
        cmd = CommandStream(
            getcwd(),
            None,
            self.result,
            ["tail", "-n", "5"]
            )
        with self.assertRaises(ValueError):
            self.tail.exec(cmd)

    def testTailNoNumberOption(self):
        cmd = CommandStream(
            getcwd(),
            None,
            self.result,
            ["tail", "-n", "b", "TailFile.txt"]
        )
        with self.assertRaises(ValueError):
            self.tail.exec(cmd)

    def testTailInvalidOption(self):
        with self.assertRaises(ValueError):
            self.tail.exec(
                CommandStream(
                    getcwd(),
                    None,
                    self.result,
                    ["tail", "-t", "TailFile.txt"]
                )
            )

    def testTailStringStdin(self):
        stdin = StringIO("AAA\nABB\nCCC")
        command = CommandStream(
            getcwd(),
            stdin,
            self.result,
            ["tail", "-n", "2"]
            )
        self.tail.exec(command)
        stdout = command.getStdout().getvalue()
        self.assertEqual(stdout, "ABB\nCCC\n")


class TestUniq(unittest.TestCase):
    def setUp(self) -> None:
        self.uniq = Uniq()
        self.result = StringIO()
        with open("UniqFile.txt", "w") as f:
            f.write("AAA\nAAA\naaa\nBBB\nBBB")
        with open("UniqStdin.txt", "w") as f:
            f.write("CCC\nCCC\nccc\nDDD\nDDD\n")

    def tearDown(self) -> None:
        remove("UniqFile.txt")
        remove("UniqStdin.txt")

    def testUniqFile(self):
        cmd = CommandStream(
            getcwd(),
            None,
            self.result,
            ["uniq", "UniqFile.txt"]
            )
        self.uniq.exec(cmd)
        stdout = cmd.getStdout().getvalue()
        self.assertEqual(stdout, "AAA\naaa\nBBB\n")

    def testUniqFileWithIgnore(self):
        cmd = CommandStream(
            getcwd(),
            None,
            self.result,
            ["uniq", "-i", "UniqFile.txt"]
            )
        self.uniq.exec(cmd)
        stdout = cmd.getStdout().getvalue()
        self.assertEqual(stdout, "AAA\nBBB\n")

    def testUniqStdin(self):
        stdin = open("UniqStdin.txt", "r")
        cmd = CommandStream(
            getcwd(),
            stdin,
            self.result,
            ["uniq"]
            )
        self.uniq.exec(cmd)
        stdout = cmd.getStdout().getvalue()
        self.assertEqual(stdout, "CCC\nccc\nDDD\n")

    def testUniqStdinWithIgnore(self):
        stdin = open("UniqStdin.txt", "r")
        cmd = CommandStream(
            getcwd(),
            stdin,
            self.result,
            ["uniq", "-i"]
            )
        self.uniq.exec(cmd)
        stdout = cmd.getStdout().getvalue()
        self.assertEqual(stdout, "CCC\nDDD\n")

    def testUniqFileNotFound(self):
        cmd = CommandStream(
            getcwd(),
            None,
            self.result,
            ["uniq", "-i", "file1.txt"]
            )
        with self.assertRaises(FileNotFoundError):
            self.uniq.exec(cmd)

    def testUniqMissingStdin(self):
        cmd = CommandStream(
            getcwd(),
            None,
            self.result,
            ["uniq", "-i"]
            )
        with self.assertRaises(ValueError):
            self.uniq.exec(cmd)

    def testUniqStringStdin(self):
        stdin = StringIO("AAA\nAAA\nCCC")
        cmd = CommandStream(
            getcwd(),
            stdin,
            self.result,
            ["uniq"]
            )
        self.uniq.exec(cmd)
        stdout = cmd.getStdout().getvalue()
        self.assertEqual(stdout, "AAA\nCCC\n")


class TestWc(unittest.TestCase):
    def setUp(self) -> None:
        self.wc = Wc()
        self.result = StringIO()
        with open("WcFileA.txt", "w") as f:
            f.write("AA BB\nCC")
        with open("WcFileB.txt", "w") as f:
            f.write("AA BB\nCC")
        with open("WcStdin.txt", "w") as f:
            f.write("AA BB\nCC")

    def tearDown(self) -> None:
        remove("WcFileA.txt")
        remove("WcFileB.txt")
        remove("WcStdin.txt")

    def testWcFile(self):
        cmd = CommandStream(
            getcwd(),
            None,
            self.result,
            ["wc", "WcFileA.txt"]
        )
        self.wc.exec(cmd)
        stdout = cmd.getStdout().getvalue()
        self.assertEqual(stdout, "2\n3\n8\n")

    def testWcStdin(self):
        stdin = open("WcStdin.txt", "r")
        cmd = CommandStream(
            getcwd(),
            stdin,
            self.result,
            ["wc"]
        )
        self.wc.exec(cmd)
        stdout = cmd.getStdout().getvalue()
        self.assertEqual(stdout, "2\n3\n8\n")

    def testWcFileMOption(self):
        cmd = CommandStream(
            getcwd(),
            None,
            self.result,
            ["wc", "-m", "WcFileA.txt"]
        )
        self.wc.exec(cmd)
        stdout = cmd.getStdout().getvalue()
        self.assertEqual(stdout, "8\n")

    def testMulitiWcFileMOption(self):
        cmd = CommandStream(
            getcwd(),
            None,
            self.result,
            ["wc", "-m", "WcFileA.txt", "WcFileB.txt"]
        )
        self.wc.exec(cmd)
        stdout = cmd.getStdout().getvalue()
        self.assertEqual(stdout, "16\n")

    def testWcStdinMOption(self):
        stdin = open("WcStdin.txt", "r")
        cmd = CommandStream(
            getcwd(),
            stdin,
            self.result,
            ["wc", "-m"]
        )
        self.wc.exec(cmd)
        stdout = cmd.getStdout().getvalue()
        self.assertEqual(stdout, "8\n")

    def testWcFileWOption(self):
        cmd = CommandStream(
            getcwd(),
            None,
            self.result,
            ["wc", "-w", "WcFileA.txt"]
        )
        self.wc.exec(cmd)
        stdout = cmd.getStdout().getvalue()
        self.assertEqual(stdout, "3\n")

    def testMulitiWcFileWOption(self):
        cmd = CommandStream(
            getcwd(),
            None,
            self.result,
            ["wc", "-w", "WcFileA.txt", "WcFileB.txt"]
        )
        self.wc.exec(cmd)
        stdout = cmd.getStdout().getvalue()
        self.assertEqual(stdout, "6\n")

    def testWcStdinWOption(self):
        stdin = open("WcStdin.txt", "r")
        cmd = CommandStream(
            getcwd(),
            stdin,
            self.result,
            ["wc", "-w"]
        )
        self.wc.exec(cmd)
        stdout = cmd.getStdout().getvalue()
        self.assertEqual(stdout, "3\n")

    def testWcFileLOption(self):
        cmd = CommandStream(
            getcwd(),
            None,
            self.result,
            ["wc", "-l", "WcFileA.txt"]
        )
        self.wc.exec(cmd)
        stdout = cmd.getStdout().getvalue()
        self.assertEqual(stdout, "2\n")

    def testMulitiWcFileLOption(self):
        cmd = CommandStream(
            getcwd(),
            None,
            self.result,
            ["wc", "-l", "WcFileA.txt", "WcFileB.txt"]
        )
        self.wc.exec(cmd)
        stdout = cmd.getStdout().getvalue()
        self.assertEqual(stdout, "4\n")

    def testWcStdinLOption(self):
        stdin = open("WcStdin.txt", "r")
        cmd = CommandStream(
            getcwd(),
            stdin,
            self.result,
            ["wc", "-l"]
        )
        self.wc.exec(cmd)
        stdout = cmd.getStdout().getvalue()
        self.assertEqual(stdout, "2\n")

    def testWcStringStdin(self):
        stdin = StringIO("AAA")
        command = CommandStream(
            getcwd(),
            stdin,
            self.result,
            ["wc", "-l"]
            )
        self.wc.exec(command)
        stdout = command.getStdout().getvalue()
        self.assertEqual(stdout, "1\n")

    def testWcMissingStdin(self):
        cmd = CommandStream(
            getcwd(),
            None,
            self.result,
            ["wc", "-l"]
            )
        with self.assertRaises(ValueError):
            self.wc.exec(cmd)

    def testWcFileNotFound(self):
        cmd = CommandStream(
            getcwd(),
            None,
            self.result,
            ['wc', 'WcNoFile.txt']
        )
        with self.assertRaises(FileNotFoundError):
            self.wc.exec(cmd)


if __name__ == "__main__":
    unittest.main()

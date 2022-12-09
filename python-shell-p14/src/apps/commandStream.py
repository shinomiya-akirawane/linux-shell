import sys
from typing import TextIO, List


class CommandStream:
    def __init__(
        self, currDir: str, stdin=None, stdout=sys.stdout, args: List[str] = []
    ):
        self.currDir = currDir
        self.stdout: TextIO = stdout
        self.stdin: TextIO = stdin
        self.args = args
        self.files: list[str] = []
        self.options: dict = {}
        self.pattern: str = ""
        self.path: str = ""
        self.content: str = ""
        self.appName = args[0]

        if self.appName == "pwd" or self.appName == "_pwd":
            # args contains appName
            # pwd cannot have more than one command line arguments
            if len(args) > 1:
                raise ValueError("wrong number of command line arguments")

        elif self.appName == "cd" or self.appName == "_cd":
            # cd must have PATH specified
            if len(args) != 2:
                raise ValueError("wrong number of command line arguments")

            self.setPath(args[1])

        elif self.appName == "ls" or self.appName == "_ls":
            # ls cannot have two PATHs specified
            if len(args) > 2:
                raise ValueError("wrong number of command line arguments")

            if len(args) == 2:
                self.setPath(args[1])

        elif self.appName == "cat" or self.appName == "_cat":
            if len(args) > 1:
                for file in args[1:]:
                    self.addFiles(file)

        elif self.appName == "echo" or self.appName == "_echo":
            # echo must hace ARG specified
            if len(args) == 1:
                raise ValueError("wrong number of command line arguments")

            for elem in args[1:]:
                self.content += elem + " "

            self.content = self.content.rstrip(" ")

        elif (
            self.appName == "head"
            or self.appName == "tail"
            or self.appName == "_head"
            or self.appName == "_tail"
        ):
            if len(args) > 4:
                raise ValueError("wrong number of command line arguments")

            # both OPTIONS and FILES are specified
            if len(args) == 4:
                if args[1] == "-n":
                    self.addOptions(args[1].lstrip("-"), args[2])
                    self.addFiles(args[3])
                else:
                    raise ValueError("invalid option")

            # only OPTION is specified
            elif len(args) == 3:
                if args[1] != "-n":
                    raise ValueError("invalid option")

                if "-" in args[1]:
                    self.addOptions(args[1].lstrip("-"), args[2])
                else:
                    raise ValueError("invalid option")

            # only FILE is specified
            elif len(args) == 2:
                self.addFiles(args[1])

        elif self.appName == "grep" or self.appName == "_grep":
            # grep must have PATTERN specified
            if len(args) < 2:
                raise ValueError("wrong number of command line arguments")

            self.pattern = args[1]
            if len(args) > 2:
                for file in args[2:]:
                    self.addFiles(file)

        elif self.appName == "cut" or self.appName == "_cut":
            # cut must have OPTIONS specified
            if len(args) < 3 or len(args) > 4:
                raise ValueError("wrong number of command line arguments")

            if "-" in args[1]:
                self.addOptions(args[1].lstrip("-"), args[2])
            else:
                raise ValueError("invalid option")

            # if FILE is specified
            if len(args) == 4:
                self.addFiles(args[3])

        elif self.appName == "find" or self.appName == "_find":
            # find must have -name and PATTERN specified
            if len(args) < 3 or len(args) > 4:
                raise ValueError("wrong number of command line arguments")
            if "-name" not in args:
                raise ValueError("invalid usage")

            if args[2] == "-name":
                self.setPath(args[1])
                if len(args) == 4:
                    self.setPattern(args[3])

            elif args[1] == "-name" and len(args) == 3:
                self.setPattern(args[2])

        elif self.appName == "uniq" or self.appName == "_uniq":
            if len(args) > 3:
                raise ValueError("wrong number of command line arguments")
            # both OPTIONS and FILE are specified
            if len(args) == 3:
                if args[1] == "-i":
                    self.addOptions(args[1].lstrip("-"), "")
                    self.addFiles(args[2])
                else:
                    raise ValueError("invalid option")
            # only OPTIONS or FILE is specified
            elif len(args) == 2:
                if args[1] == "-i":
                    self.addOptions(args[1].lstrip("-"), "")
                else:
                    self.addFiles(args[1])

        elif self.appName == "sort" or self.appName == "_sort":
            if len(args) > 3:
                raise ValueError("wrong number of command line arguments")
            # both OPTIONS and FILE are specified
            if len(args) == 3:
                if args[1] == "-r":
                    self.addOptions(args[1].lstrip("-"), "")
                    self.addFiles(args[2])
                else:
                    raise ValueError("invalid option")
            # only OPTIONS or FILE is specified
            elif len(args) == 2:
                if args[1] == "-r":
                    self.addOptions(args[1].lstrip("-"), "")
                else:
                    self.addFiles(args[1])

        elif self.appName == "wc" or self.appName == "_wc":
            # only OPTIONS or FILE is specified
            if len(args) == 2:
                if args[1] == "-m" or args[1] == "-w" or args[1] == "-l":
                    self.addOptions(args[1].lstrip("-"), "")
                else:
                    self.addFiles(args[1])
            # both OPTIONS and FILE are speficied
            elif len(args) == 3:
                if args[1] == "-m" or args[1] == "-w" or args[1] == "-l":
                    self.addOptions(args[1].lstrip("-"), "")
                    self.addFiles(args[2])
                else:
                    raise ValueError('invalid option')
            # more than one FILE are specified
            elif len(args) > 3:
                if args[1] == "-m" or args[1] == "-w" or args[1] == "-l":
                    self.addOptions(args[1].lstrip("-"), "")
                    for elem in args[2:]:
                        self.addFiles(elem)
                else:
                    raise ValueError('invalid option')

        else:
            raise ValueError("invalid command")

    # for testing only
    def __eq__(self, anotherStream):
        if self.getStdin() and anotherStream.getStdin():
            stdin = self.getStdin().name
            anotherStdin = anotherStream.getStdin().name
        elif self.getStdin() is None and anotherStream.getStdin() is None:
            stdin = 1
            anotherStdin = 1
        else:
            stdin = 1
            anotherStdin = 2
        if (
            self.getCurrDir() == anotherStream.getCurrDir()
            and (
                (stdin == anotherStdin)
                or (stdin in anotherStdin)
                or (anotherStdin in stdin)
            )
            and (
                (self.getStdout().name == anotherStream.getStdout().name)
                or (self.getStdout().name in anotherStream.getStdout().name)
                or (anotherStream.getStdout().name in self.getStdout().name)
            )
            and self.getFiles() == anotherStream.getFiles()
            and self.getPattern() == anotherStream.getPattern()
            and self.getAllOptions() == anotherStream.getAllOptions()
            and self.getContent() == anotherStream.getContent()
            and self.getCurrDir() == anotherStream.getCurrDir()
            and self.getPath() == anotherStream.getPath()
        ):
            return True
        return False

    def setCurrDir(self, currDir: str) -> None:
        self.currDir = currDir

    def getCurrDir(self) -> List[str]:
        return self.currDir

    def getAppName(self) -> str:
        return self.appName

    def getContent(self) -> str:
        return self.content

    def getFiles(self) -> List[str]:
        return self.files[:]

    def addFiles(self, arg: str) -> None:
        self.files.append(arg)

    def addOptions(self, key: str, val) -> None:
        self.options[key] = val

    def setPattern(self, pattern: str) -> None:
        self.pattern = pattern

    def setPath(self, path: str) -> None:
        self.path = path

    def getOptions(self, key: str):
        return self.options[key]

    def getAllOptions(self):
        return self.options

    def getStdout(self) -> TextIO:
        return self.stdout

    def setStdout(self, stdout: TextIO) -> None:
        self.stdout = stdout

    def getStdin(self) -> TextIO:
        return self.stdin

    def setStdin(self, stdin: TextIO) -> None:
        self.stdin = stdin

    def getPath(self) -> str:
        return self.path

    def getPattern(self) -> str:
        return self.pattern

    def getArgs(self) -> List[str]:
        return self.args

    def addArg(self, arg) -> None:
        self.args.append(arg)

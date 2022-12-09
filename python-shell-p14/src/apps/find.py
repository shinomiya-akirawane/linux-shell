from os import walk, path
from fnmatch import fnmatch
from apps.commandStream import CommandStream
from apps.application import Application


class Find(Application):
    def exec(self, command: CommandStream):
        pattern = command.getPattern()

        # if no PATH is specified
        if command.getPath() == "":
            directory = "."
        else:
            directory = command.getPath()

        stdoutContent = ""
        isFileMatch = False
        for root, dirs, files in walk(directory):
            for file in files:
                if fnmatch(file, pattern):
                    stdoutContent += path.join(root, file) + "\n"
                    isFileMatch = True

        if not isFileMatch:
            raise FileNotFoundError("no match found")

        command.getStdout().write(stdoutContent)

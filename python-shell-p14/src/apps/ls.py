from os import getcwd, listdir
from apps.commandStream import CommandStream
from apps.application import Application


class Ls(Application):
    def exec(self, command: CommandStream):
        directory = command.getPath()

        # if no PATH is specified
        if directory == "":
            directory = getcwd()

        try:
            files = listdir(directory)
        except Exception:
            raise FileNotFoundError(f"no such file or directory: {directory}")

        stdoutContentLst = []
        for file in files:
            if not file.startswith("."):
                stdoutContentLst.append(file)
                stdoutContentLst.sort()

        stdoutContent = "\n".join(stdoutContentLst) + "\n"

        command.getStdout().write(stdoutContent)

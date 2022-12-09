from io import StringIO
from apps.commandStream import CommandStream
from apps.application import Application


class Tail(Application):
    def exec(self, command: CommandStream):
        files = command.getFiles()
        stdin = command.getStdin()
        stdoutContent = ""

        try:
            lines = command.getOptions("n")
            try:
                numberOfLines = int(lines)
            except Exception:
                raise ValueError("wrong parameter type")
        except KeyError:
            numberOfLines = 10

        if files == []:
            try:
                if type(stdin) == StringIO:
                    stingIOInContents = stdin.getvalue()
                    stingIOInContents = stingIOInContents.strip("\n")
                    inContents = stingIOInContents.split("\n")
                # stdin is TextIO type
                else:
                    inContents = stdin.readlines()
            except Exception:
                raise ValueError("missing stdin")
        else:
            for file in files:
                try:
                    with open(file, "r") as f:
                        inContents = f.readlines()
                except Exception:
                    raise FileNotFoundError(
                        f"no such file or directory: {file}"
                        )

            length = len(inContents)
            for n in range(0, length):
                # check if all the element in the list end with "\n"
                content = inContents[n]
                if not content.endswith("\n"):
                    content += "\n"
                    inContents[n] = content

        length = min(len(inContents), numberOfLines)

        for n in range(0, length):
            stdoutContent += inContents[len(inContents) - length + n]
            if not stdoutContent.endswith("\n"):
                stdoutContent += "\n"

        command.getStdout().write(stdoutContent)

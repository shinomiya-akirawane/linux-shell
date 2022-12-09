from io import StringIO
from apps.commandStream import CommandStream
from apps.application import Application


class Uniq(Application):
    def exec(self, command: CommandStream):
        stdoutContent = ""
        stdin = command.getStdin()
        files = command.getFiles()
        ignoreFlag = False
        if "i" in command.options.keys():
            ignoreFlag = True

        if files == []:
            try:
                if type(stdin) == StringIO:
                    stingIOInContents = stdin.getvalue()
                    stingIOInContents = stingIOInContents.strip("\n")
                    inContents = stingIOInContents.split("\n")
                else:  # stdin is TextIO type
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
        # check if all the element in the list end with "\n"
        for n in range(0, length):
            content = inContents[n]
            if not content.endswith("\n"):
                content += "\n"
                inContents[n] = content

        if ignoreFlag:
            firstline = inContents[0].upper()
            stdoutContent += firstline
        else:
            firstline = inContents[0]
            stdoutContent += firstline

        for n in range(1, len(inContents)):
            lastLine = inContents[n - 1]
            currentLine = inContents[n]
            if ignoreFlag:
                lastLine = lastLine.upper()
                currentLine = currentLine.upper()
            if lastLine != currentLine:
                stdoutContent += currentLine

        command.getStdout().write(stdoutContent)

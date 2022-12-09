from io import StringIO
from apps.commandStream import CommandStream
from apps.application import Application


class Sort(Application):
    def exec(self, command: CommandStream):
        stdoutContent = ""
        stdin = command.getStdin()
        files = command.getFiles()

        reverseFlag = False
        if "r" in command.options.keys():
            reverseFlag = True

        if files == []:
            try:
                if type(stdin) == StringIO:
                    stingIOInContents = stdin.getvalue()
                    stingIOInContents = stingIOInContents.rstrip("\n")
                    inContents = stingIOInContents.split("\n")
                # stdin is TextIO type
                else:
                    inContents = stdin.readlines()
            except Exception:
                raise ValueError("Missing Stdin")
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

        inContents.sort()

        if reverseFlag:
            inContents.reverse()
            for Content in inContents:
                stdoutContent += Content

        else:
            for Content in inContents:
                stdoutContent += Content

        command.getStdout().write(stdoutContent)

from io import StringIO
from apps.commandStream import CommandStream
from apps.application import Application


class Wc(Application):
    def exec(self, command: CommandStream):
        stdoutContent = ""
        stdin = command.getStdin()
        files = command.getFiles()

        mFlag = False
        wFlag = False
        lFlag = False

        mCounter = 0
        wCounter = 0
        lCounter = 0

        # to separate files
        extraNumberAdded = 0

        if "m" in command.getAllOptions():
            mFlag = True
        elif "w" in command.getAllOptions():
            wFlag = True
        elif "l" in command.getAllOptions():
            lFlag = True

        if files == []:
            try:
                if type(stdin) == StringIO:
                    inContents = stdin.getvalue()
                # stdin is TextIO type
                else:
                    textIOInContents = stdin.readlines()
                    inContents = "".join(textIOInContents)
            except Exception:
                raise ValueError("missing stdin")
        else:
            inContents = ""
            for file in files:
                try:
                    with open(file, "r") as f:
                        inContents += f.read()
                        if not inContents.endswith("\n"):
                            inContents += "\n"
                            extraNumberAdded += 1

                except Exception:
                    raise FileNotFoundError(
                        f"no such file or directory: {file}"
                        )

        mCounter = len(inContents) - extraNumberAdded

        lines = inContents.strip('\n').split('\n')
        for line in lines:
            words = line.strip(' ').split(' ')
            wCounter += len(words)

        lCounter = len(lines)

        if mFlag:
            stdoutContent = str(mCounter) + '\n'
        elif wFlag:
            stdoutContent = str(wCounter) + '\n'
        elif lFlag:
            stdoutContent = str(lCounter) + '\n'
        else:
            stdoutContent += str(lCounter) + '\n'
            stdoutContent += str(wCounter) + '\n'
            stdoutContent += str(mCounter) + '\n'

        command.getStdout().write(stdoutContent)

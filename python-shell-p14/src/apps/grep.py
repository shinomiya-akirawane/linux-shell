from re import match
from io import StringIO
from apps.commandStream import CommandStream
from apps.decorator import GlobbingDecorator
from apps.application import Application


class Grep(Application):
    def exec(self, command: CommandStream):
        stdoutContent = ""
        pendingAdd = ""
        pattern = command.getPattern()
        files = command.getFiles()
        files = GlobbingDecorator.globbing(files)
        stdin = command.getStdin()

        numberOfFiles = len(files)

        # if no FILE is specified
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

            length = len(inContents)
            for n in range(0, length - 1):
                # check if all the element in the list end with "\n"
                content = inContents[n]
                if not content.endswith("\n"):
                    content += "\n"
                    inContents[n] = content

            for content in inContents:
                if match(pattern, content):
                    pendingAdd = content
                    if not pendingAdd.endswith("\n"):
                        pendingAdd += "\n"
                    stdoutContent += pendingAdd

        elif numberOfFiles == 1:
            s_file = files[0]
            try:
                with open(s_file, "r") as f:
                    SingleFileContents = f.readlines()
                    for content in SingleFileContents:
                        if match(pattern, content):
                            pendingAdd = content
                            if not pendingAdd.endswith("\n"):
                                pendingAdd += "\n"
                            stdoutContent += pendingAdd
            except Exception:
                raise FileNotFoundError(
                    f"no such file or directory: {s_file}"
                    )

        else:
            for m_file in files:
                try:
                    with open(m_file, "r") as f:
                        MultiFileContents = f.readlines()
                        for content in MultiFileContents:
                            if match(pattern, content):
                                pendingAdd = f"{m_file}:{content}"
                                if not pendingAdd.endswith("\n"):
                                    pendingAdd += "\n"
                                stdoutContent += pendingAdd
                except Exception:
                    raise FileNotFoundError(
                        f"no such file or directory: {m_file}"
                        )

        command.getStdout().write(stdoutContent)

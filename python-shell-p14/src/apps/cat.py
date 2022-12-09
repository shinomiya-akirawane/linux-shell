from io import StringIO

from apps.application import Application
from apps.decorator import GlobbingDecorator
from apps.commandStream import CommandStream


class Cat(Application):
    def exec(self, command: CommandStream):
        files = command.getFiles()
        files = GlobbingDecorator.globbing(files)
        stdin = command.getStdin()

        stdOutContent = ""
        # No files are specified
        if len(files) == 0:
            try:
                if type(stdin) == StringIO:
                    stdOutContent = stdin.getvalue()
                # stdin is TextIO type
                else:
                    stdOutContent = stdin.read()
            except Exception:
                raise ValueError("missing stdin")
        else:
            for file in files:
                try:
                    with open(file, "r") as f:
                        stdOutContent += f.read()

                        if not stdOutContent.endswith("\n"):
                            stdOutContent += "\n"
                except Exception:
                    raise FileNotFoundError(
                        f"no such file or directory: {file}"
                        )

        command.getStdout().write(stdOutContent)

from io import StringIO
from apps.commandStream import CommandStream
from apps.application import Application


class Cut(Application):
    def exec(self, command: CommandStream):
        try:
            byte_range = command.getOptions("b")
            if " " in byte_range:
                raise ValueError("byte option should not contain whitespace")
            else:
                byte_range = byte_range.split(",")
        except Exception:
            raise ValueError("invalid option")

        for b in byte_range:
            if "-" in b:
                nums = b.split("-")
                for n in nums:
                    if not n.isdigit() and n != "":
                        raise ValueError("invalid range")
            else:
                if not b.isdigit():
                    raise ValueError("invalid range")

        # if no FILE is specified
        if command.getFiles() == []:
            try:
                if type(command.getStdin()) == StringIO:
                    fileContent = command.getStdin().getvalue()
                else:
                    stdinContent = command.getStdin().readlines()
                    fileContent = "".join(stdinContent)
            except Exception:
                raise ValueError("missing stdin")

        else:
            file = command.getFiles()[0]
            with open(file, "r") as f:
                fileContent = f.read()

        allStdoutContent = ""
        fileContent_lines = fileContent.rstrip("\n").split("\n")
        for line in fileContent_lines:
            stdoutContent = [""] * len(line)
            for b in byte_range:
                if "-" in b:
                    # if the end of the range is specified (eg. -5)
                    if b[0] == "-":
                        pos = int(b[1:])
                        if pos < len(line):
                            for i in range(pos):
                                stdoutContent[i] = line[i]
                        else:
                            for i in range(len(line)):
                                stdoutContent[i] = line[i]
                    # if the start of the range is specified (eg. 3-)
                    elif b[-1] == "-":
                        pos = int(b[:-1])
                        if pos < len(line):
                            for i in range(pos - 1, len(line)):
                                stdoutContent[i] = line[i]
                    # if both ends of the range is specified (eg. 3-5)
                    else:
                        num = b.split("-")
                        start = int(num[0]) - 1
                        end = int(num[1])
                        if start < len(line) and end <= len(line):
                            for i in range(start, end):
                                stdoutContent[i] = line[i]
                        elif start < len(line) and end > len(line):
                            for i in range(start, len(line)):
                                stdoutContent[i] = line[i]

                # if no range is specified (eg. 1,2)
                else:
                    pos = int(b) - 1
                    if pos < len(line):
                        stdoutContent[pos] = line[pos]

            allStdoutContent += "".join(stdoutContent) + "\n"

        command.getStdout().write(allStdoutContent)

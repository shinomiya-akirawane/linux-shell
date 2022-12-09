from os import getcwd
from apps.commandStream import CommandStream
from apps.application import Application


class Pwd(Application):
    def exec(self, command: CommandStream):
        cwd = getcwd()
        command.getStdout().write(cwd + "\n")

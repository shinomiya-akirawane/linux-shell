from io import StringIO

from appFactory import AppFactory
from apps.commandStream import CommandStream


class Command:
    def eval(self):
        pass


class Call(Command):
    def __init__(self, commandStream: CommandStream):
        self.commandStream = commandStream
        self.app = AppFactory.create(commandStream.getAppName())

    def eval(self):
        self.app.exec(self.commandStream)


class Pipe(Command):
    def __init__(self, leftCmd, rightCmd: Call, commandStream):
        self.commandStream = commandStream
        self.leftCmd = leftCmd
        self.rightCmd = rightCmd

    def eval(self):
        # stringIO is used to store the leftCmd output temporarily
        tempStdout = StringIO()
        if type(self.leftCmd) == Pipe:
            self.rightCmd.commandStream.setStdin(tempStdout)
            self.leftCmd.rightCmd.commandStream.setStdout(tempStdout)
        self.leftCmd.commandStream.setStdout(tempStdout)
        self.leftCmd.eval()
        self.rightCmd.commandStream.setStdin(
                                    self.leftCmd.commandStream.getStdout()
                                    )
        self.rightCmd.eval()


class Seq(Command):
    def __init__(self, firstCommand):
        self.commands = [firstCommand]

    def addCommand(self, command):
        self.commands.append(command)

    def eval(self):
        for command in self.commands:
            command.eval()

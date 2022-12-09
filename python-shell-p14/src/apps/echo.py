from apps.commandStream import CommandStream
from apps.decorator import GlobbingDecorator
from apps.application import Application


class Echo(Application):
    def exec(self, command: CommandStream):
        args = command.getContent()
        argsList = []
        argsList.append(args)
        argsList = GlobbingDecorator.globbing(argsList)
        for args in argsList:
            echoContent = args + "\n"
            command.getStdout().write(echoContent)

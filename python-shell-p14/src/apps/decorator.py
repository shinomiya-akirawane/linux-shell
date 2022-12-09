from sys import exc_info
from glob import glob
from typing import List
from .application import Application


class UnsafeDecorator(Application):
    def __init__(self, app):
        self.app = app

    def exec(self, command):
        stdout = command.getStdout()
        try:
            self.app.exec(command)
        except Exception:
            error = exc_info()[1]
            print(str(error))
            stdout.write(str(error) + "\n")
            return error


class GlobbingDecorator:
    def globbing(commandArgs: List[str]):
        argsBeforeGlob = commandArgs
        argsAfterGlob = []
        for Args in argsBeforeGlob:
            globbed = glob(Args)
            if globbed:
                argsAfterGlob.extend(globbed)
                argsAfterGlob.sort()
            else:
                argsAfterGlob.append(Args)

        return argsAfterGlob

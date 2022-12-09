from os import chdir, getcwd
from apps.commandStream import CommandStream
from apps.application import Application


class Cd(Application):
    def exec(self, command: CommandStream):
        destination = command.getPath()

        try:
            chdir(destination)
            cwd = getcwd()
            command.setCurrDir(cwd)
        except Exception:
            raise FileNotFoundError(
                f"no such file or directory: {destination}"
                )

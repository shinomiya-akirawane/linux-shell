from .commandStream import CommandStream
from abc import ABC, abstractmethod


class Application(ABC):
    @abstractmethod
    def exec(self, command: CommandStream):
        pass

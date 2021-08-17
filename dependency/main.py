from dataclasses import dataclass
from dependency.list import List
from dependency.remove import Remove
from dependency.install import Install
from dependency.depend import Depend


class Dependency(List, Remove, Install, Depend):
    lines = []

    def __init__(self, lines: list) -> None:
        with open("dependency.config", "r") as file:
            data = file.read()
        self.lines = lines

    def play(self)-> list:
        _output = list(map(self._select_action, self.lines))
        return _output

    def _select_action(self, line: str) -> str:
        _methods = filter(lambda x: "_" not in x, self.__dir__())
        for method in self.__dir__():
            if method in line.lower():
                return getattr(self, method)(line)
    
    @dataclass
    class PackageObject:
        name: str
        depend: list = []

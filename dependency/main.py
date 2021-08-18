import json
from dataclasses import dataclass
from dependency.list import List
from dependency.remove import Remove
from dependency.install import Install
from dependency.depend import Depend

from collections.abc import Iterable
from uuid import uuid4

class Dependency(List, Remove, Install, Depend):
    _dependency_file = "dependency.config"

    def __init__(self, lines: list) -> None:
        self.lines = []
        self.packages = []

        try:
            with open(self._dependency_file, "r") as file:
                self._read_data(file.read().split("\n"))
        except (FileNotFoundError, json.decoder.JSONDecodeError) as e:
            pass
        
        self.lines = lines

    def play(self)-> list:
        _output = list(map(self._select_action, self.lines))
        with open(self._dependency_file, "w") as file:
            _data = "\n".join(list(map(str, self.packages)))
            file.write(_data)
        return _output

    def _select_action(self, line: str) -> str:
        _methods = filter(lambda x: "_" not in x, self.__dir__())
        for method in self.__dir__():
            if method == line.lower().strip().split()[0]:
                return getattr(self, method)(line)
    
    def end(self, line: str) -> str:
        return "END"

    def create_package(self, name: str) -> object:
        _package = self._read_package_by_name(name)
        if _package:
            return _package
        else:
            _package = self.PackageObject(name, new=True)
            self.packages.append(_package)
            return _package
        
    def _read_package_by_name(self, name: str) -> object:
        return next(filter(lambda x: x.name.upper() == name.upper(), self.packages), None)

    def _read_package_by_id(self, _id: str, packages: list) -> object:
        return next(filter(lambda x: x._id == _id, packages), None)

    def _read_data(self, data: list) -> None:
        _packages = list(map(self.PackageObject, data))
        for _package in _packages:
            if _package.depend:
                _package.depend = list(map(lambda x: self._read_package_by_id(x, _packages), _package.depend))
        self.packages = _packages

    class PackageObject:
        _id: str = None
        name: str = None
        installed: bool = False
        
        def __init__(self, data: str, new: bool = False) -> None:
            self.depend = []

            if new:
                self.__create__(data)
            else:
                self.__load__(data)
        
        def __repr__(self):
            return f"<id: {self._id} name:{self.name}>"

        def __load__(self, data: str) -> None:
            _data = json.loads(data)
            for key, value in _data.items():
                if hasattr(self, key):
                    if key == "depend":
                        setattr(self, key, value)
                    else:
                        setattr(self, key, value)
        
        def __create__(self, data: str) -> None:
            self._id = str(uuid4())
            self.name = data

        def __add_dependency__(self, _object: object):
            self.depend.append(_object)

        def __iter__(self) -> Iterable:
            for key in self.__dir__():
                if key.startswith("__"):
                    continue
                elif key == "depend":
                    yield key, list(map(lambda x: x._id, getattr(self, key)))
                else:
                    yield key, getattr(self, key)

        def __str__(self) -> str:
            return json.dumps(dict(self))

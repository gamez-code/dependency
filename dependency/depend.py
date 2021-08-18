import string

class Depend(object):

    def depend(self, line: str) -> str:
        _, _package, *dependencies = list(filter(lambda x: x not in string.whitespace, line.upper().split()))
        _package_object = self.create_package(_package)
        return self.add(_package_object, dependencies)

    def add(self, _package_object: object, dependencies: list) -> str:
        for dependency in dependencies:
            _dependency = self.create_package(dependency)
            if _dependency not in _package_object.depend:
                _package_object.__add_dependency__(
                        _dependency
                    )
        return f"DEPEND {_package_object.name} {' '.join(list(map(lambda x: x.name, _package_object.depend)))}"
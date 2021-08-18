import string


class PackageNotRemoved(Exception):
    def __init__(self, msg):
        return f"Could not be removed, {msg}"

class Remove(object):

    def remove(self, line: str = None, package: object = None) -> str:
        if line:
            _, _package = list(filter(lambda x: x not in string.whitespace, line.split()))
            package = self.create_package(_package)
        return f"REMOVE {package.name}\n" + self._make_remove(package)

    def _someone_depend_on_me(self, _package_object: object) -> bool:
        packages_installed = filter(lambda x: x.installed, self.packages)
        depend_on = filter(lambda x: _package_object in x.depend, packages_installed)
        return True if next(depend_on, False) else False

    def _execute_remove(self, _package_object: object) -> str:
        try:
            responses = self._remove_package(_package_object)
        except PackageNotRemoved:
            return f"   {_package_object.name} could not be removed"
        return responses

    def _depend_remove(self, _packages: list) -> str:
        response = ""
        for _package in _packages:
            depend_on_me = self._someone_depend_on_me(_package)
            if _package.installed and not depend_on_me:
                response += f"\n   {_package.name} is no longer needed\n" + self._execute_remove(_package)
        return response

    def _make_remove(self, _package_object: object) -> str:
        if not _package_object.installed:
            return f"   {_package_object.name} is not installed"

        depend_on_me = self._someone_depend_on_me(_package_object)
        if depend_on_me:
            return f"   {_package_object.name} is still needed"
        
        return self._execute_remove(_package_object)

    def _remove_package(self, package: object) -> str:
        try:
            response = self._os_remove(package.name)
            if not response:
                raise PackageNotRemoved
            package.installed = False
            return f"   {package.name} successfully removed" + self._depend_remove(package.depend)
        except Exception:
            raise PackageNotInstalled

    def _os_remove(self, name: str) -> bool:
        # TODO hacer con apt, pip, npm, poner retry.
        return True
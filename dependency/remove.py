
class PackageNotRemoved(Exception):
    def __init__(self, msg):
        return f"Could not be removed, {msg}"

class Remove(object):

    def remove(self, line: str = None, package: object = None) -> str:
        if line:
            _, _package = list(filter(lambda x: x not in string.whitespace, line.upper().split()))
            package = self.create_package(_package)
        return self._make_remove(_package)

    def _make_remove(self, _package_object: object) -> str:
        if not _package_object.installed:
            return f"INSTALL {_package_object.name}\n   {_package_object.name} is not installed"

        packages_installed = filter(lambda x: x.installed, self.packages)
        depend_on = filter(lambda x: _package_object in x.depend, packages_installed)
        if next(depend_on, None):
            return f"INSTALL {_package_object.name}\n   {_package_object.name} is still needed"
        
        try:
            responses = self._remove_package(_package_object)
        except PackageNotRemoved:
            return f"{_package_object.name} could not be removed"
        return responses

    def _remove_package(self, package: object) -> str:
        try:
            response = self._os_remoded(package.name)
            if not response:
                raise PackageNotRemoved
            package.installed = False
            return f"   {package.name} successfully removed"
        except Exception:
            raise PackageNotInstalled

    def _os_removed(self, name: str) -> bool:
        # TODO hacer con apt, pip, npm, poner retry.
        return True
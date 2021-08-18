import string
 
class PackageNotInstalled(Exception):
    def __init__(self, msg):
        return f"Could not be installed, {msg}"

class Install(object):
    def install(self, line: str) -> object:
        _, _package = list(filter(lambda x: x not in string.whitespace, line.upper().split()))
        _package_object = self.create_package(_package)
        return self._make_installation(_package_object)

    def _make_installation(self, _package_object: object) -> str:
        try:
            _dependencies = [self._install_package(d) for d in _package_object.depend]
        except PackageNotInstalled:
            _dependencies = [self.remove(package=d) for d in _package_object.depend]
            return f"INSTALL {package.name}\n   {_package_object.name} could not be installed"
        _dependencies.append(self._install_package(_package_object))
        return "\n".join(_dependencies)

    def _install_package(self, package: object) -> str:
        try:
            if not package.installed:
                response = self._os_installed(package.name)
                if not response:
                    raise PackageNotInstalled
                package.installed = True
                return f"INSTALL {package.name}\n   {package.name} successfully installed"
            return f"INSTALL {package.name}\n   {package.name} is already installed"
        except Exception:
            raise PackageNotInstalled
            
    
    def _os_installed(self, name: str) -> bool:
        # TODO hacer con apt, pip, npm, poner retry.
        return True
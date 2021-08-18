import string
 
class PackageNotInstalled(Exception):
    def __init__(self, msg):
        return f"Could not be installed, {msg}"

class Install(object):
    def install(self, line: str) -> object:
        _, _package = list(filter(lambda x: x not in string.whitespace, line.split()))
        _package_object = self.create_package(_package)
        return self._make_installation(_package_object)

    def _make_installation(self, _package_object: object) -> str:
        response = [f"INSTALL {_package_object.name}"]
        try:
            _dependencies = [self._install_package(d) for d in _package_object.depend]
        except PackageNotInstalled:
            _dependencies = [self.remove(package=d) for d in _package_object.depend]
            return response + [f"   {_package_object.name} could not be installed"]
        _dependencies.append(self._install_package(_package_object, principal=True))
        return "\n".join(list(filter(lambda x: x, response + _dependencies)))

    def _install_package(self, package: object, principal: bool = False) -> str:
        try:
            if not package.installed:
                response = self._os_installed(package.name)
                if not response:
                    raise PackageNotInstalled
                package.installed = True
                return f"   {package.name} successfully installed"
            if principal:
                return f"   {package.name} is already installed"
            return ""
        except Exception:
            raise PackageNotInstalled
            
    
    def _os_installed(self, name: str) -> bool:
        # TODO hacer con apt, pip, npm, poner retry.
        return True
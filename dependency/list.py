
class List(object):
    def list(self, *args) -> str:
        return "\n  ".join(["LIST"] + list(map(lambda x: x.name, filter(lambda x: x.installed, self.packages))))
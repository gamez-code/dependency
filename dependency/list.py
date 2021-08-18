
class List(object):
    def list(self, *args) -> str:
        return list(map(lambda x: x.name, filter(lambda x: x.installed, self.packages)))
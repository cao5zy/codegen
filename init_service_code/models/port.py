
class Port:
    def __init__(self, json):
        self.__json = json
    @property
    def host(self):
        return self.__json["host"] if "host" in self.__json.keys() else None
    @property
    def container(self):
        return self.__json["container"] if "container" in self.__json.keys() else None

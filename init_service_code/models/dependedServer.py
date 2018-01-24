from .nameRule import validateName

class DependedServer:
    def __init__(self, json):
        self.__json = json

    @property
    @validateName
    def name(self):
        return self.__json["name"]

    @property
    @validateName
    def localName(self):
        return self.__json["localName"]

    @property
    def type(self):
        return self.__json["type"]

def getDependedServers(serviceJson):
    return map(lambda n:DependedServer(n), serviceJson["dependedServers"]) if "dependedServers" in serviceJson.keys() and serviceJson["dependedServers"] else None

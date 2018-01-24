from .serviceParam import ServiceParam

class ServiceMethod:
    def __init__(self, methodJson):
        self.__methodJson = methodJson
    @property
    def name(self):
        return self.__methodJson["name"]
    @property
    def params(self):
        return list(map(lambda p:ServiceParam(p), self.__methodJson["params"]) if "params" in self.__methodJson and self.__methodJson["params"] else [])

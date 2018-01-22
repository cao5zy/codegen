from .serviceMethod import ServiceMethod

class ServiceInterface:
    def __init__(self, interfaceJson):
        self.__interfaceJson = interfaceJson
    @property
    def name(self):
        return self.__interfaceJson["name"]
    @property
    def methods(self):
        return list(map(lambda m:ServiceMethod(m), self.__interfaceJson["methods"]))

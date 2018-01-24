class ServiceParam:
    def __init__(self, paramJson):
        self.__paramJson = paramJson
    @property
    def name(self):
        return self.__paramJson["name"]
    @property
    def type(self):
        return self.__paramJson["type"]
    @property
    def isUrlFilter(self):
        return (lambda name:False if name not in self.__paramJson.keys() else self.__paramJson[name] == "True" or self.__paramJson[name] == True)\
            ("isUrlFilter")
    @property
    def defaultVal(self):
        return (lambda name:None if name not in self.__paramJson.keys() else self.__paramJson[name])("defaultVal")

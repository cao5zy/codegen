from .deployConfig import DeployConfig
from .serviceInterface import ServiceInterface
from .dependedServer import DependedServer
from .port import Port
from .config import ConfigValue

class ServiceProject:
    def __init__(self, json):
        self.__deployConfig = None
        self.__serviceInterface = None
        self.__json = json
        self.getJson = lambda:json

    @property
    def deployConfig(self):
        def loadDeployConfig():
            self.__deployConfig = DeployConfig(self.__json)
            return self.__deployConfig
        
        return self.__deployConfig if self.__deployConfig else loadDeployConfig()
    
    @property
    def serviceInterface(self):
        def loadServiceInterface():
            if "interface" in self.__json.keys() and self.__json["interface"]:
                self.__serviceInterface = ServiceInterface(self.__json["interface"])

            return self.__serviceInterface
        
        return self.__serviceInterface if self.__serviceInterface else loadServiceInterface()

    @property
    def port(self):
        return Port(self.__json["port"]) if "port" in self.__json.keys() else None
    

    @property
    def name(self):
        return self.deployConfig.name

    @property
    def dependedServers(self):
        return list(map(lambda n:DependedServer(n), self.__json["dependedServers"])) \
            if "dependedServers" in self.__json.keys() and self.__json["dependedServers"] \
               else []

    @property
    def configs(self):
        return list(map(lambda n:ConfigValue(n, self.__json["config"][n]), self.__json["config"].keys())) if "config" in self.__json.keys() else []


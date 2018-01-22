from .defaultConfig import DefaultConfig

class Index:
    def __init__(self, serviceProject, allServiceProjects):
        self.__serviceProject = serviceProject
        self.__defaultConfig = DefaultConfig(serviceProject, allServiceProjects)

    @property
    def portName(self):
        return self.__defaultConfig.port.name

    @property
    def pluginName(self):
        return self.__serviceProject.serviceInterface.name
    

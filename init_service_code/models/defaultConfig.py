from .config import ConfigValue

class DefaultConfig:
    def __init__(self, serviceProject, allServiceProjects):
        self.__serviceProject = serviceProject
        self.__allServiceProjects = allServiceProjects

    @property
    def port(self):
        return ConfigValue("port", self.__serviceProject.port.container)
    
    @property
    def dependedServers(self):
        return (list(map(lambda n:ConfigValue('''%sHost'''%n.localName, '''http://%s'''%n.localName) , \
                        filter(lambda n:n.type in ["db", "service"], self.__serviceProject.dependedServers))) if self.__serviceProject.dependedServers != None else []) +\
    (list(map(lambda n:ConfigValue('''%sPort''' % n.localName, list(filter(lambda x:x.name == n.name, self.__allServiceProjects))[0].port.container) , \
              filter(lambda n:n.type in ["db", "service"], self.__serviceProject.dependedServers))) if self.__serviceProject.dependedServers != None else [])
    
    @property
    def configs(self):
        return list(map(lambda n:ConfigValue('''%s'''% n.name, n.value), self.__serviceProject.configs)) if self.__serviceProject.configs != None else []
    

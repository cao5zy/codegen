from ..defaultConfig import DefaultConfig

class ConfigGenerator:
    def __init__(self, serviceProject, allServiceProjects):
        self.__serviceProject = serviceProject
        self.__allServiceProjects = allServiceProjects
        
    def gen(self):
        defaultConfig = DefaultConfig(self.__serviceProject, self.__allServiceProjects)
        return "{" + ",\n".join(
            list(map(lambda n:'''"%s": "%s"''' % (n.name, n.value), filter(lambda n:isinstance(n.value, str) or isinstance(n.value, unicode), defaultConfig.dependedServers + defaultConfig.configs))) +\
            list(map(lambda n:'''"%s": %s''' % (n.name, n.value), filter(lambda n:isinstance(n.value, int) or isinstance(n.value, float), defaultConfig.dependedServers + defaultConfig.configs))) +\
            ['''"{self.name}": {self.value}'''.format(self=defaultConfig.port)]) + "}"

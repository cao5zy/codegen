from ..defaultConfig import DefaultConfig

class ConfigModuleGenerator:
    def __init__(self, serviceProject, allServiceProjects):
        self.__serviceProject = serviceProject
        self.__allServiceProjects = allServiceProjects

    def gen(self):
        defaultConfig = DefaultConfig(self.__serviceProject, self.__allServiceProjects)
        
        return '''
(function (global, factory) {
    module.exports = factory(require('config'));
}(global, function (config) {
    return {
%s
    };
    
})); ''' % ",\n".join(list(map(lambda n:"    " * 2 + n,\
                list(map(lambda n:'''{name}: config.get("{name}")'''.format(name = n.name), defaultConfig.dependedServers)) \
                      + ['''{self.name}: config.get("{self.name}")'''.format(self=defaultConfig.port)] \
                      + list(map(lambda n:'''{name}: config.get("{name}")'''.format(name=n.name), defaultConfig.configs)))))

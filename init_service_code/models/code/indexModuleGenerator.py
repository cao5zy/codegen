from ..index import Index
from jinja2 import Template

class IndexModuleGenerator:
    def __init__(self, serviceProject, allServiceProjects):
        self.__index = Index(serviceProject, allServiceProjects)

    def gen(self):
        return '''
(function (global, factory) {{
        module.exports = factory(require('seneca'), require('./conf'), require('./{self.pluginName}'));
        }}(global, function (seneca, conf, {self.pluginName}) {{
    const service = seneca();

    service.use({self.pluginName});
    console.log('service start to listen port:', conf.{self.portName});

    service.listen({{port: conf.{self.portName}}});
}}));
 '''.format(self = self.__index)

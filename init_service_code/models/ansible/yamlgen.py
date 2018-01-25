
# model definition

class YamlGenModel:
    class Service:
        def __init__(self, name = None, entrypoint = None, image = None, recreate = None, restart = None, ports = None, volumes = None):
            self.name = name # key of service, it would be mapped to the deployconfig.name
            self.entrypoint = entrypoint
            self.image = image
            self.recreate = recreate
            self.restart = restart
            self.ports = ports
            self.volumes = volumes
            
    def __init__(self, services = []):
        self.services = services


# model definition
def convertToModel(json):
    def genService(deployJson):
        return YamlGenModel.Service( name = deployJson["name"], \
                                     entrypoint = deployJson["entrypoint"] if "entryoint" in deployJson else None, \
                                     image = "%s:%s" % (deployJson["image"], deployJson["image_tag"]), \
                                     ports = [deployJson["port"]], \
                                     recreate = deployJson["recreate"], \
                                     restart = deployJson["restart"], \
                                     volumes = list(map(lambda n:n["container"], deployJson["volumes"])) if "volumes" in deployJson else None \
        )
    return YamlGenModel([genService(serviceJson["deployConfig"]) for serviceJson in json])

def genAnsibleConfig(parentPath, yamlGenModel):
    pass

def genHosts(parentPath, yamlGenModel):
    pass

def genTaskFolder(rolePath):
    import util
    print(rolePath)
    print(rolePath[0])
    return util.createFolder("tasks", rolePath)

def genRoot(parentPath, yamlGenModel):
    genAnsibleConfig(parentPath, yamlGenModel)
    genHosts(parentPath, yamlGenModel)
    [genTaskMain(genTaskFolder(result[0]), result[1]) for result in genRoleFolder(parentPath, yamlGenModel)]
    
# gen code for service
def genRoleFolder(parentPath, yamlGenModel):
    import util
    def genRolesFolder():
        return util.createFolder("roles", parentPath)

    def genContent(rolesFolder):
        def gen(serviceName):
            return util.createFolder(serviceName, rolesFolder)

        return list(map(lambda service: (gen(service.name), service), yamlGenModel.services))

    return genContent(genRolesFolder())

class BlockBuilder:
    
    def __init__(self, desc, ansible_module):
        from jinja2 import Template
        import os
        
        items = []

        def genPrint(value):
            return " %s" % value if isinstance(value, int) or isinstance(value, float) else ''' "%s"''' % value
        def genValueStr(value):
            return os.linesep + os.linesep.join(list(map(lambda n:"      -%s" % genPrint(n), value))) if isinstance(value, list) and not isinstance(value, str) else genPrint(value)
        
        def add(key, value):
            items.append((key, genValueStr(value)))
            return self
        
        def gen():
            return Template('''- name: {{ desc }}
  {{ ansible_module }}:

''').render(desc = desc, ansible_module = ansible_module) \
        + Template('''{% for (key, value) in items %}    {{ key }}:{{ value }}
{% endfor %}
''').render(items = items)

        self.add = add
        self.gen = gen


def genTaskMain(parentPath, service):
    import os
    import util
    def genItems(builder):
        [builder.add(key, service.__dict__[key]) for key in service.__dict__ if service.__dict__[key] != None]
        return builder
                        
    def genDockerScript():
        return (lambda builder:genItems(builder).gen())(BlockBuilder("%s docker container" % service.name, "docker_container"))
    return util.writeContent(os.path.join(parentPath, "main.yaml"), "---%s%s%s...%s" % (os.linesep, \
                                                                               genDockerScript(), \
                                                                                        os.linesep, os.linesep))


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
def convertToModel(json, rootFolder):
    def genService(deployJson):
        def genVolume(container):
            return "%s:%s" % (container, "%s/%s/app" % (rootFolder, deployJson["name"])) if rootFolder else container
        
        return YamlGenModel.Service( name = deployJson["name"], \
                                     entrypoint = deployJson["entrypoint"] if "entryoint" in deployJson else None, \
                                     image = "%s:%s" % (deployJson["image"], deployJson["image_tag"]), \
                                     ports = [deployJson["port"]], \
                                     recreate = deployJson["recreate"], \
                                     restart = deployJson["restart"], \
                                     volumes = list(map(lambda n:genVolume(n["container"]), deployJson["volumes"])) if "volumes" in deployJson else None \
        )
    return YamlGenModel([genService(serviceJson["deployConfig"]) for serviceJson in json])

def genAnsibleConfig(parentPath, yamlGenModel):
    import util
    import os
    util.writeContent(os.path.join(parentPath, "ansible.cfg"), ConfigBuilder().addSection("defaults") \
                      .addKeyValue("inventory", "hosts") \
                      .gen())
                            
def genHosts(parentPath, yamlGenModel):
    import util
    import os
    util.writeContent(os.path.join(parentPath, "hosts"), ConfigBuilder().addSection("local") \
                      .addKey("localhost") \
                      .gen())

def genTaskFolder(rolePath):
    import util
    print(rolePath)
    print(rolePath[0])
    return util.createFolder("tasks", rolePath)

def genRoot(parentPath, yamlGenModel):
    import util
    def gen(ansibleFolder):
        genAnsibleConfig(ansibleFolder, yamlGenModel)
        genHosts(ansibleFolder, yamlGenModel)
        genEntry(ansibleFolder, yamlGenModel)
        [genTaskMain(genTaskFolder(result[0]), result[1]) for result in genRoleFolder(ansibleFolder, yamlGenModel)]

    gen(util.createFolder("ansible", parentPath))
    
# gen code for service
def genEntry(ansibleFolder, yamlGenModel):
    import os
    import util
    util.writeContent(os.path.join(ansibleFolder, "site.yaml"), \
        "---%s%s%s...%s" % (os.linesep, BlockBuilder() \
        .addTitle("hosts", "local") \
        .add("roles", list(map(lambda service:service.name, yamlGenModel.services))) \
        .gen() \
                        , os.linesep, os.linesep))
    

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
    
    def __init__(self, defaultIndent = 0):
        from jinja2 import Template
        import os
        indent = 0
        space = '  '
        items = []

        def genPrint(value):
            return '' if value == None else " %s" % value if isinstance(value, int) or isinstance(value, float) else ''' "%s"''' % value

        def add(key, value = None, level = 1):
            if isinstance(value, list) and not isinstance(value, str):
                items.append("%s%s:" % ((defaultIndent + level) * space, key))
                [items.append("%s-%s" % ( (defaultIndent + level + 1) * space, genPrint(val))) for val in value]
            else:
                items.append("%s%s:%s" % ((defaultIndent + level) * space, key, genPrint(value)))

            return self

        def addTitle(key, value):
            items.append("%s- %s: %s" % (defaultIndent * space, key, value))

            return self
            
        def gen():
            return Template('''{% for item in items %}{{ item }}
{% endfor %}
''').render(items = items)

        self.add = add
        self.gen = gen
        self.addTitle = addTitle
        
class ConfigBuilder:
    def __init__(self):
        from jinja2 import Template
        items = []
        
        def addSection(name):
            items.append("[%s]" % name)
            return self

        def addKey(name):
            items.append(name)
            return self
            
        def addKeyValue(key, value):
            items.append("%s=%s" % (key, value))
            return self
        
        def gen():
            return Template('''{% for item in items %}{{ item }}
{% endfor %}''').render(items = items)

        self.addSection = addSection
        self.addKeyValue = addKeyValue
        self.addKey = addKey
        self.gen = gen
        
def genTaskMain(parentPath, service):
    import os
    import util
    def genItems(builder):
        [builder.add(key, service.__dict__[key], 2) for key in service.__dict__ if service.__dict__[key] != None]
        return builder
                        
    def genDockerScript():
        return (lambda builder:genItems(builder).gen())(BlockBuilder().addTitle("name", "%s docker container" % service.name).add("docker_container"))
    return util.writeContent(os.path.join(parentPath, "main.yaml"), "---%s%s%s...%s" % (os.linesep, \
                                                                               genDockerScript(), \
                                                                                        os.linesep, os.linesep))

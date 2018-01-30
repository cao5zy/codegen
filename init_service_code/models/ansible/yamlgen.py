# model definition
class YamlGenModel:
    class Service:
        def __init__(self, name = None, entrypoint = None, image = None, recreate = None, restart = None, ports = None, volumes = None, links = None):
            self.name = name # key of service, it would be mapped to the deployconfig.name
            self.entrypoint = entrypoint
            self.image = image
            self.recreate = recreate
            self.restart = restart
            self.ports = ports
            self.volumes = volumes
            self.links = links

    class Relation:
        def __init__(self, name = None, depend = None):
            self.name = name
            self.depend = depend
            
    def __init__(self, services = [], relations = [], isDebug = True):
        self.services = services
        self.relations = relations
        self.isdebug = isDebug


# model definition
def genLinks(yamlGenModel):
    from itertools import groupby
    import flattener
    import copy

    getKeys = lambda : [item[0] for item in groupby(yamlGenModel.relations, lambda n:n.name)]
    getDependencies = lambda key: flattener.flatten([list(map(lambda x:x.depend, item[1])) for item in groupby(yamlGenModel.relations, lambda n:n.name) if item[0] == key])
    genLinks = lambda oldService: None if oldService.name not in getKeys() else \
        list(map(lambda n:"%s:%s" % (n,n), getDependencies(oldService.name)))
    genService = lambda oldService: YamlGenModel.Service( \
                                                          name = oldService.name,
                                                          entrypoint = oldService.entrypoint,
                                                          image = oldService.image,
                                                          recreate = oldService.recreate,
                                                          restart = oldService.restart,
                                                          ports = oldService.ports,
                                                          volumes = oldService.volumes,
                                                          links = genLinks(oldService)
    )

    noLinksService = lambda : [service for service in yamlGenModel.services if service.name not in getKeys()]
    haveLinksService = lambda : [genService(service) for service in yamlGenModel.services if service.name in getKeys()]
    return YamlGenModel(
        noLinksService() + haveLinksService(),
        yamlGenModel.relations
    )

class ConvertOption:
    def __init__(self, isDebug = True, rootFolder = None):
        self.isdebug = isDebug
        self.rootfolder = rootFolder
    
def convertToModel(json, convertoption):
    import flattener
    def genService(deployJson):
        def genVolume(container):
            return "%s:%s" % ("%s/%s/app" % (convertoption.rootfolder, deployJson["name"]), container) if convertoption.isdebug and convertoption.rootfolder else container
        
        return YamlGenModel.Service( name = deployJson["name"], \
                                     entrypoint = deployJson["entrypoint"] if "entrypoint" in deployJson else None, \
                                     image = "%s:%s" % (deployJson["image"], deployJson["image_tag"]), \
                                     ports = ['%s:%s' % (deployJson["port"], deployJson["port"])] if convertoption.isdebug else [deployJson["port"]], \
                                     recreate = deployJson["recreate"], \
                                     restart = deployJson["restart"], \
                                     volumes = list(map(lambda n:genVolume(n["container"]), deployJson["volumes"])) if "volumes" in deployJson else None \
        )

    def genRelation(serviceJson):
        def gen():
            return [YamlGenModel.Relation( name = serviceJson["deployConfig"]["name"], depend = item["name"]) for item in serviceJson["dependedServers"]]
        
        return [] if not "dependedServers" in serviceJson else gen()


    
    return genLinks(YamlGenModel([genService(serviceJson["deployConfig"]) for serviceJson in json], flattener.flatten([genRelation(serviceJson) for serviceJson in json]), \
                                 convertoption.isdebug))

def genAnsibleConfig(parentPath, yamlGenModel):
    import util
    import os
    util.writeContent(os.path.join(parentPath, "ansible.cfg"), ConfigBuilder().addSection("defaults") \
                      .addKeyValue("inventory", "hosts") \
                      .addSection("privilege_escalation") \
                      .addKeyValue("become", "True") \
                      .addKeyValue("become_method", "sudo") \
                      .gen())
                            
def genHosts(parentPath, yamlGenModel):
    import util
    import os
    util.writeContent(os.path.join(parentPath, "hosts"), ConfigBuilder().addSection("local") \
                      .addKey("localhost") \
                      .gen())

def genTaskFolder(rolePath):
    import util
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
        .addTitle("hosts", "localhost" if yamlGenModel.isdebug else "") \
        .add("roles", list(map(lambda service:service.name, yamlGenModel.services))) \
        .gen() \
                        , os.linesep, os.linesep))

def sortServicesByDependency(services, relations):
    class entry:
        def __init__(self, name, dependencies):
            self.name = name
            self.dependencies = dependencies
    def putEmptyToResult(result, objs):
        for obj in filter(lambda obj:obj["dependencies"] == None or (type(obj["dependencies"]) == list and len(obj["dependencies"]) == 0), objs):
            result.append(obj["project"])
        return result

    def clearEmptyKeys(result, objs):
        return list(filter(lambda obj:obj["dependencies"] != None and type(obj["dependencies"]) == list and len(obj["dependencies"]) > 0, objs))

    def removeKeys(result, objs):
        def removekey(obj):
            obj["dependencies"] = list(key for key in obj["dependencies"] if key not in result)
            return obj
    
        return list(map(lambda obj:removekey(obj), objs))
    
    
    def sortByDependency(result, objs):
        return result if len(objs) == 0 else sortByDependency(result, \
            removeKeys(result, clearEmptyKeys(putEmptyToResult(result, objs), objs)))

    def completeEntries(entries):
        import flattener
        [entries.append({"project": n, "dependencies": []}) \
         for n in flattener.flatten(list(map(lambda x:x["dependencies"], entries))) \
             if len(list(filter(lambda x:x["project"] == n, entries))) == 0]

        return entries
    
    def genEntries():
        from itertools import groupby
        return [{"project": item[0], "dependencies": list(map(lambda n:n.depend, item[1]))} for item in groupby(relations, lambda x:x.name)]

    return list(map(lambda name:list(filter(lambda n:n.name == name, services))[0], sortByDependency([], completeEntries(genEntries()))))


def genRoleFolder(parentPath, yamlGenModel):
    import util
    def genRolesFolder():
        return util.createFolder("roles", parentPath)

    def genContent(rolesFolder):
        def gen(serviceName):
            return util.createFolder(serviceName, rolesFolder)

        return list(map(lambda service: (gen(service.name), service), sortServicesByDependency(yamlGenModel.services, yamlGenModel.relations)))

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

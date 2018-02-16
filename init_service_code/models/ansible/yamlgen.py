# model definition
import logging
from pipe import *

class YamlGenModel:
    class Service:
        MetaProperties = ["hostWorkingPath", "type"]
        def __init__(self, name = None, entrypoint = None, image = None, recreate = None, restart = None, ports = None, volume = None, links = None, type = None, hostWorkingPath = None):
            self.name = name # key of service, it would be mapped to the deployconfig.name
            self.entrypoint = entrypoint
            self.image = image
            self.recreate = recreate
            self.restart = restart
            self.ports = ports
            self.volume = volume
            self.links = links
            self.type = type
            self.hostWorkingPath = hostWorkingPath
            
    class Relation:
        def __init__(self, name = None, depend = None):
            self.name = name
            self.depend = depend

    def __init__(self, services = [], relations = [], isDebug = True, deployRootPath = None, proxyName = "nginx_proxy"):
        self.services = services
        self.relations = relations
        self.isdebug = isDebug
        self.deployRootPath = deployRootPath
        self.proxyname = proxyName

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
                                                          volume = oldService.volume,
                                                          links = genLinks(oldService),
                                                          type = oldService.type,
                                                          hostWorkingPath = oldService.hostWorkingPath
                                                          
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

def genHostWorkingPath(root, serviceName, isService):
    genDbWorkingPath = lambda: "{root}/{serviceName}/db".format(root = root, serviceName = serviceName)
    genMicroServiceWorkingPath = lambda: "{root}/{serviceName}/app".format(root = root, serviceName = serviceName)

    return genMicroServiceWorkingPath() if isService else genDbWorkingPath()

def isMicroService(deployJson):
    return "instanceType" in deployJson and deployJson["instanceType"] == "microService"

def isFrontApp(deployJson):
    return "instanceType" in deployJson and deployJson["instanceType"] == "frontApp"

def genVolume(container, deployJson, convertoption):
    return "{hostFolder}:{containerFolder}".format(hostFolder = genHostWorkingPath(convertoption.rootfolder, deployJson["name"], isMicroService(deployJson) or isFrontApp(deployJson)) , containerFolder = container) if convertoption.isdebug else container

def genProxy(yamlGenModel):
    def gen(name = "nginx_proxy"):
        def workingPath():
            return "{root}/{name}".format(root = yamlGenModel.deployRootPath, name = name)

        def volumes():
            return ["{workingPath}/logs:/etc/nginx/logs".format(workingPath = workingPath())] \
                + ["{workingPath}/conf.d:/etc/nginx/conf.d".format(workingPath = workingPath())]

        def links():
            return yamlGenModel.services \
                | where(lambda n:n.type in ["microService", "frontApp"]) \
                | select(lambda n:"{name}:{name}".format(name = n.name)) \
                | as_list()

        return YamlGenModel.Service(name = name, \
                                    image = "nginx:1.12", \
                                    ports = ["80:80"], \
                                    type = "proxy", \
                                    volume = volumes(), \
                                    links = links()
        )

    return YamlGenModel(services = yamlGenModel.services + [gen()], \
                        relations = yamlGenModel.relations, isDebug = yamlGenModel.isdebug, deployRootPath = yamlGenModel.deployRootPath)

def convertToModel(json, convertoption):
    import flattener
    def genService(deployJson):
        
        return YamlGenModel.Service( name = deployJson["name"], \
                                     entrypoint = deployJson["entrypoint"] if "entrypoint" in deployJson else None, \
                                     image = "%s:%s" % (deployJson["image"], deployJson["image_tag"]), \
                                     ports = ['%s:%s' % (deployJson["port"], deployJson["port"])] if convertoption.isdebug else [deployJson["port"]], \
                                     recreate = deployJson["recreate"], \
                                     restart = deployJson["restart"], \
                                     volume = genVolume(deployJson["volume"], deployJson, convertoption) if "volume" in deployJson else None, \
                                     type = deployJson["instanceType"],
                                     hostWorkingPath = genHostWorkingPath(convertoption.rootfolder, deployJson["name"], isMicroService(deployJson))
        )


    def genRelation(serviceJson):
        def gen():
            return [YamlGenModel.Relation( name = serviceJson["deployConfig"]["name"], depend = item["name"]) for item in serviceJson["dependedServers"]]
        
        return [] if not "dependedServers" in serviceJson or serviceJson["dependedServers"] == None else gen()


    
    return genProxy(genLinks(YamlGenModel([genService(serviceJson["deployConfig"]) for serviceJson in json], flattener.flatten([genRelation(serviceJson) for serviceJson in json]), \
                                 convertoption.isdebug, convertoption.rootfolder)))

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

def genProxyAnsible(yamlGenModel):
    import os
    def volumes():
        return yamlGenModel.proxy.volumes \
            | select(lambda n:'''"{n.host}:{n.container}"'''.format(n=n)) \
            | as_list() \
            if yamlGenModel.proxy and yamlGenModel.proxy.volumes else []
    def links():
        return yamlGenModel.proxy.links \
            | select(lambda n:'''"{n.host}:{n.container}"'''.format(n=n)) \
            | as_list() \
            if yamlGenModel.proxy and yamlGenModel.proxy.links else []

    return "---{sep}{content}{sep}...{sep}".format(sep = os.linesep, content = BlockBuilder().addTitle("name", "nginx proxy container") \
        .add("docker_container") \
        .add("name", "proxy_server", 1) \
        .add("image", "nginx:1.12", 1) \
        .add("volumes", volumes(), 1) \
        .add("links", links(), 1) \
        .gen())
        

def genRoot(parentPath, yamlGenModel):
    import util
    import os
    def gen(ansibleFolder):
        def genRoles(rolesFolder):
            genAnsibleConfig(ansibleFolder, yamlGenModel)
            genHosts(ansibleFolder, yamlGenModel)
            genEntry(ansibleFolder, yamlGenModel)
            [genTaskMain(genTaskFolder(result[0]), result[1]) for result in genRoleFolder(rolesFolder, yamlGenModel)]

            # util.writeContent("%s/main.yaml" % genTaskFolder(os.path.join(rolesFolder, yamlGenModel.proxyname)), genProxyAnsible(yamlGenModel))

        return genRoles(genRolesFolder(ansibleFolder))
        

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

        def contains(item, lst):
            return lst | any(lambda x:x["project"] == item)

        @Pipe
        def concatOrigin(lst):
            return lst + [n for n in entries if not contains(n["project"], lst)]

        @Pipe
        def concatNoDependencies(lst):
            return lst + [{"project": n.name, "dependencies": []} for n in services if not contains(n.name, lst)]
        
        def gen():
            return [{"project": n, "dependencies": []} \
                 for n in flattener.flatten(list(map(lambda x:x["dependencies"], entries))) if not contains(n, entries)] \
                     | concatOrigin \
                     | concatNoDependencies
        
        return gen()

    
    def genEntries():
        from itertools import groupby
        return [{"project": item[0], "dependencies": list(map(lambda n:n.depend, item[1]))} for item in groupby(relations, lambda x:x.name)]

    result = services if len(relations) == 0 else \
             list(map(lambda name:list(filter(lambda n:n.name == name, services))[0], sortByDependency([], completeEntries(genEntries()))))

    assert len(result) == len(services)

    return result

def genRolesFolder(parentPath):
    import util
    return util.createFolder("roles", parentPath)

def genRoleFolder(rolesFolder, yamlGenModel):
    import util

    def genContent():
        def gen(serviceName):
            return util.createFolder(serviceName, rolesFolder)

        return list(map(lambda service: (gen(service.name), service), sortServicesByDependency(yamlGenModel.services, yamlGenModel.relations)))

    return genContent()

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
        [builder.add(key, service.__dict__[key], 2) for key in service.__dict__ if key not in YamlGenModel.Service.MetaProperties and service.__dict__[key] != None]
        return builder
    
    def genDockerContent(builder):
        return genItems( \
                         builder.addTitle("name", "%s docker container" % service.name).add("docker_container") \
                         )
    def genDbFolder(builder):
        return (builder.addTitle("name", "init db folder") \
                .add("file") \
                .add("path", service.hostWorkingPath, 2) \
                .add("state", "directory", 2) \
                )
    
    def gen(builder):
        return genDockerContent(builder) if service.type in ["microService", "frontApp"] else genDockerContent(genDbFolder(builder))

    return util.writeContent(os.path.join(parentPath, "main.yaml"), "---{sep}{content}{sep}...{sep}".format(sep = os.linesep, content = gen(BlockBuilder()).gen()))

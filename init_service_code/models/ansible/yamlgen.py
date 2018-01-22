
# model definition

class YamlGenModel:
    class Service:
        def __init__(self, name = ""):
            self.name = name # key of service, it would be mapped to the deployconfig.name
    def __init__(self):
        self.services = []


# model definition

# gen code for service
def genRoleFolder(parentPath, yamlGenModel):
    import util
    def gen(serviceName):
        return util.createFolder(serviceName, parentPath)
    
    return (list(map(lambda service: gen(service.name), yamlGenModel.services)), yamlGenModel)
    

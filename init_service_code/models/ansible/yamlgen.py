
# model definition

class YamlGenModel:
    class Service:
        def __init__(self, name = ""):
            self.name = name # key of service, it would be mapped to the deployconfig.name
    def __init__(self):
        self.services = []


# model definition

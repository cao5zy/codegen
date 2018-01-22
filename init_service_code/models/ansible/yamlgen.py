
# model definition

class YamlGenModel:
    class Service:
        def __init__(self, name = "", entrypoint = "", image = "", recreate = False, restart = False, ports = [], volumes = []):
            self.name = name # key of service, it would be mapped to the deployconfig.name
            self.entrypoint = entrypoint
            self.image = image
            self.recreate = recreate
            self.restart = restart
            self.ports = ports
            self.volumes = volumes
            
    def __init__(self):
        self.services = []


# model definition

# gen code for service
def genRoleFolder(parentPath, yamlGenModel):
    import util
    def gen(serviceName):
        return util.createFolder(serviceName, parentPath)
    
    return (list(map(lambda service: gen(service.name), yamlGenModel.services)), yamlGenModel)

class BlockBuilder:
    
    def __init__(self, name, ansible_module):
        from jinja2 import Template

        items = []

        def genPrint(value):
            return value if isinstance(value, int) or isinstance(value, float) else '''"%s"''' % value
        def genValueStr(value):
            return "\n" + "\r".join(list(map(lambda n:"    - %s" % genPrint(n), value))) if isinstance(value, list) and not isinstance(value, str) else genPrint(value)
        
        def add(key, value):
            if key == "name" and value != name:
                raise ValueError("value of %s should be equal to %s if key is name" % (value, name))
            
            items.append((key, genValueStr(value)))
            return self
        
        def gen():
            return Template('''- name: build {{ name}} container
  {{ ansible_module }}:

''').render(name = name, ansible_module = ansible_module) \
        + Template('''{% for (key, value) in items %} 
    {{ key }}: {{ value }}
{% endfor %}
''').render(items = items)

        self.add = add
        self.gen = gen


def genTaskMain(parentPath, service):

    template = '''---
- name: deploy {{ name }} service
  docker_container:
    

...
'''
    

from models.ansible.rootGenerator import getEntries
from jinja2 import Template

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

def getDependencies(jsons):
    return list(map(lambda json:{"project":json["deployConfig"]["name"], \
                             "dependencies": \
                                 None if "dependedServers" not in json.keys() or json["dependedServers"] == None else list(map(lambda d:d["name"], json["dependedServers"]))}, jsons))
class AllGenerator:
    def __init__(self, folderPath, serviceProjects):
        def gen():
            return Template('''
---
- name: {{obj.projectname}} deployment
  hosts: dev
  become: true
  become_method: sudo

  vars:
    {% for entry in obj.entries %}
    {{entry}}
    {% endfor %}
    
  tasks:
  {% for name in obj.projectNames %}
  - include: ./{{name}}/ansible/deploy.yml
  {% endfor %}
...
 ''').render(obj={"projectNames": sortByDependency([], getDependencies(map(lambda sp:sp.getJson(), serviceProjects))),
                  "entries": getEntries(folderPath)})
        
        self.gen = gen

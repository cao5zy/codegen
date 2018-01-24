from jinja2 import Template
import re
import os
import flattener
import util

def listFiles(folderPath):
    def handleFile(handle):
        return flattener.flatten(map(lambda (root, dirs, files):handle(root, filter(lambda file:file.endswith(".yml"),files)), os.walk(folderPath)))

    return handleFile


def getEntriesFromFile(filePath):
    return list(map(lambda entry:entry.replace("{{", "").replace("}}", "").strip(), re.findall("{{[\s\w._]*}}", util.readContent(filePath))))


def getIncludes(folderPath):
    return listFiles(folderPath)(lambda root, files:files)

def getEntries(folderPath):
    return list(set(flattener.flatten(map(lambda file:populateSourcePath({'file': file, 'entries':getEntriesFromFile(file)})["entries"], \
                         listFiles(folderPath)(lambda root, files:map(lambda file: os.path.join(root, file), files))))))

def populateSourcePath(fileEntries):
    def handleSource(entry):
        return '%s: "%s"' % (entry, os.path.split(fileEntries['file'])[0] + '/../app/') \
            if fileEntries['file'].endswith('deploy.yml') and entry.endswith('source') \
               else '%s: "%s"' %(entry, "/working") if fileEntries['file'].endswith('deploy.yml') and entry.endswith('dest') \
                    else '%s: "%s"'% (entry, "")
        

    return {'file': fileEntries['file'], 'entries':list(map(lambda entry:handleSource(entry), fileEntries['entries']))}
            
    

class RootGenerator:
    def __init__(self, projectName, folderPath):

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
  {% for include in obj.includes %}
  - include: {{include}}
  {% endfor %}
...
 ''').render(obj = {"projectname": projectName,
                    "entries": getEntries(folderPath),
                    "includes": getIncludes(folderPath)
 })
        
        self.gen = gen

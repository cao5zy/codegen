from jinja2 import Template

class DependencyGenerator:
    def __init__(self, serviceProjectJson):
        def getProjectNames(name):
            return list(map(lambda dependedServer:dependedServer["name"], serviceProjectJson[name])) \
                if serviceProjectJson[name] else []
        
        def gen():
            return (lambda name:Template('''
---
{% for project in projects %}
- include: ../../{{ project }}/ansible/deploy.yml
{% endfor %}
...
''').render(projects = getProjectNames(name)) if name in serviceProjectJson.keys() else '')("dependedServers")
        
        self.gen = gen

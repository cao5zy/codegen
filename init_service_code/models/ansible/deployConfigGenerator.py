from jinja2 import Template
import flattener

class DeployConfigGenerator:
    def __init__(self, deployConfig, serviceProjectJson):
        self.__deployConfig = deployConfig

        def getConfigName():
            return deployConfig.name

        def getVolumeSource():
            return "%s_source" % getConfigName()

        def getVolumeDest():
            return "%s_dest" % getConfigName()

        def hasVolumeDefined():
            return deployConfig.volumes != None
        
        def copyScript():

            return Template('''
- name: copy {{ copy.name}} to deployment
  synchronize:
    src: "{% raw %}{{{% endraw %} {{ copy.src }} {% raw %}}}{% endraw %}"
    dest: "{% raw %}{{{% endraw %} {{ copy.dest }} {% raw %}}}{% endraw %}"
 ''').render(copy = {
     "name": getConfigName(),
     "src": getVolumeSource(),
     "dest": getVolumeDest()
 }) if self.__deployConfig.volumes != None else ""
        
            

        def gen():
            def getVolumes():
                def volumes():
                    return map(lambda volume: '- "{{ %s }}:%s"'% (getVolumeDest(), volume["container"]),  deployConfig.volumes)

                return None if not hasVolumeDefined()else ["volumes:"] + volumes()

            def getPorts():
                def port():
                    return [(lambda n: '- "%s:%s"' % (n["host"], n["container"]))(deployConfig.port)]

                return None if deployConfig.port == None else ["ports:"] + port()


            def getLinks():
                def links():
                    return map(lambda n: '- "%s:%s"' % (n["host"], n["container"]), deployConfig.links)

                return None if deployConfig.links == None else ["links:"] + links()

            dic = {
                "name": lambda:'name: "%s"' % deployConfig.name,
                "image": lambda: 'image: "%s"' % deployConfig.image,
                "volumes": lambda: getVolumes(),
                "ports": lambda: None if deployConfig.port == None else getPorts(),
                "links": lambda: None if deployConfig.links == None else getLinks(),
                "restart": lambda: None if deployConfig.restart == None else 'restart: "%s"' % deployConfig.restart,
                "recreate": lambda: None if deployConfig.recreate == None else 'recreate: "%s"' % deployConfig.recreate,
                "state": lambda: None if deployConfig.state == None else 'state: "%s"' % deployConfig.state,
                "entrypoint": lambda: None if deployConfig.entrypoint == None else 'entrypoint: "%s"' % deployConfig.entrypoint
            }



            indent = "  "
            content = Template('''
---
    {{copyScript}}

- name: initialize {{ containerName }} container
{{ indent }}docker_container:
{{ spec }}
...''').render(copyScript = copyScript(), \
                          containerName = deployConfig.name, \
                          indent = indent, \
                          spec = "\n".join(map(lambda n:indent * 2 + n, \
                                               flattener.flatten(\
                                                                 filter(lambda n:n != None,\
                                                                        map(lambda key:dic[key](), dic.keys())
                                                                 )
                                               )
                          )
                          )
    )

            return content

    

        self.gen = gen

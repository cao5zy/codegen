from jinja2 import Template
import logging

class LogConfigGenerator:
    def __init__(self, serviceProjects, dependedServers):
        self.__serviceProjects = serviceProjects
        self.__dependedServers = dependedServers

    def gen(self):
        def getLogConfig():
            return list(filter(lambda n:n.type == "logserver", self.__dependedServers))[0] \
                if len(list(filter(lambda n:n.type == "logserver", self.__dependedServers))) != 0 \
                   else None

        def hasLogConfig():
            return getLogConfig() != None

        def generateCode():
            targetServer = None
            try:
                targetServer = list(filter(lambda n:n.name == getLogConfig().name, self.__serviceProjects))[0]
            except Exception as e:
                print(e)
                raise ValueError("%s is not defined" % getLogConfig().name)

            return Template('''{
            "appenders":[{
                "type": "logstashUDP",
                "host": "{{ host }}",
                "port": {{ port }}
            }]
}''').render( host = getLogConfig().localName, port = targetServer.port.container)
            
        logging.debug({"hasLogConfig": hasLogConfig()});
 
        return None if not hasLogConfig() else generateCode()
        
        

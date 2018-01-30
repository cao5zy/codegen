#! bin/python
import os
import sys
import getopt
import demjson
from models.deployConfig import DeployConfig

def getConfig():
    return os.path.join(os.getcwd(), "md.config")

def getParam(name, default = None):
    configfile = getConfig()

    param = Param(configfile)
    
    dic = {
        "logserver": param.getParam('logServer'),
        "logserver-port": param.getParam('logServerPort')
    }

    return dic[name] if name in dic else default

def getServices():
    return Param(getConfig()).services

def getJson(file):
    return demjson.decode_file(file)
    

class Param:
    def __init__(self, configFile):
        if not os.path.exists(configFile):
            raise Exception('configuration file is not found at %s' % configFile)
        
        self.configFile = configFile

    def getJson(self, file):
        return getJson(file)
    
    def getParam(self, name):
        return self.getJson(self.configFile)[name]

    @property
    def services(self):
        return self.getJson(self.configFile)["services"]
    
    def getDeployConfig(self, name):
        pass


class Method:
    def __init__(self, json):
        pass
    

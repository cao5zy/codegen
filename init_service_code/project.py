#! /bin/python

import re
import os
import ansiblescript
import sys
from getParam import getParam
import npm
import util
from util import createSubFolder, createEmptyFile
from models.ansible.deployConfigGenerator import DeployConfigGenerator
from models.code.logConfigGenerator import LogConfigGenerator
from models.code.logModuleGenerator import LogModuleGenerator
from models.code.serviceInterfaceGenerator import ServiceInterfaceGenerator
from models.code.configGenerator import ConfigGenerator
from models.code.configModuleGenerator import ConfigModuleGenerator
from models.code.indexModuleGenerator import IndexModuleGenerator
from models.code.proxyGenerator import ProxyGenerator
from models.deployConfig import DeployConfig
from models.serviceInterface import ServiceInterface
from models.ansible.dependencyGenerator import DependencyGenerator
from models.ansible.rootGenerator import RootGenerator
import logging
from pipe import *

def getFolderName(projectName):
    return "_".join([x for x in re.split('''\s+''', projectName) if len(x.strip()) > 0])


def createProjectFolder(path):
    os.makedirs(path)
    return path

def createAnsibleFolder(path, deployConfig, serviceProject):
    result, folderPath = createSubFolder(path, "ansible")
    #create the ansbile script
    # result, testScript = createEmptyFile(folderPath, "test.yml")
    # #add the unit test to ansible script
    # ansiblescript.addBase(testScript)
    # ansiblescript.addUnitTests(testScript)

    result, deployScript = createEmptyFile(folderPath, "deploy.yml")
    util.writeContent(deployScript, DeployConfigGenerator(deployConfig, serviceProject.getJson()).gen())
        
    result, dependencyScript = createEmptyFile(folderPath, "dependencies.yml")
    util.writeContent(dependencyScript, DependencyGenerator(serviceProject.getJson()).gen())

    (lambda content, re:util.writeContent(re[1], content))\
        (RootGenerator(deployConfig.name, folderPath).gen(), createEmptyFile(folderPath, "run.yml"))



def createMicroServiceAppFolder(path,appName,  serviceProject, allServiceProjects):
    logging.debug({"appName": appName})
    
    result, folderPath = createSubFolder(path, "app")
    #add config folder
    result, configPath = createSubFolder(folderPath, "config")
    result, logConfigPath = createEmptyFile(configPath, "logconfig.json")
    util.writeContent(logConfigPath, LogConfigGenerator(allServiceProjects, serviceProject.dependedServers).gen())

    result, logModulePath = createEmptyFile(folderPath, "logger.js")
    util.writeContent(logModulePath, LogModuleGenerator(serviceProject).gen())

    result, configFilePath = createEmptyFile(configPath, "default.json")
    util.writeContent(configFilePath, ConfigGenerator(serviceProject, allServiceProjects).gen())

    result, configModulePath = createEmptyFile(folderPath, "conf.js")
    util.writeContent(configModulePath, ConfigModuleGenerator(serviceProject, allServiceProjects).gen())

    (lambda re:util.writeContent(re[1], ProxyGenerator(serviceProject).gen()))(createEmptyFile(folderPath, "proxy.js"))
    
    # add the log file and configuration    
#    log.init(sys.path[0], folderPath, appName, getParam("logserver"), getParam("logserver-port"))

    # install the npm packages
    npm.install(folderPath, appName)

    # generate the seneca plugin
    result, pluginPath = createEmptyFile(folderPath, ".".join([serviceProject.serviceInterface.name, "js"]))
    util.writeContent(pluginPath, ServiceInterfaceGenerator(serviceProject.serviceInterface).gen())

    # generate the index
    result, indexFilePath = createEmptyFile(folderPath, "index.js")
    util.writeContent(indexFilePath, IndexModuleGenerator(serviceProject, allServiceProjects).gen())


def createFrontAppFolder(projectPath, projectName):

    def downloadTemplate(projectFolder):
        import shellrun
        shellrun.run('''cd {projectfolder};
git clone https://github.com/cao5zy/ng_template.git;
cd ng_template;
git checkout 1;
rm .git -rf;
cd ..;
cp ./ng_template/template/. ./ -R;
rm ng_template -rf;
'''.format(projectfolder = projectFolder))
        
        return projectFolder

    def setProjectName(projectFolder):
        def writeContent(packageFile):
            util.writeContent(packageFile, util.readContent(packageFile).replace('''"name": "template"''', '''"name": "{name}"'''.format(name = projectName)))
            return projectFolder

        return writeContent(os.path.join(projectFolder, "package.json"))
    
    return [createProjectFolder(os.path.join(projectPath, projectName))] | select(lambda n:downloadTemplate(n)) \
        | select(lambda n: setProjectName(n)) \
        | first

def generateCode(parentPath, serviceProject, allServiceProjects):
    deployConfig = serviceProject.deployConfig

    projectName = lambda : deployConfig.name
    projectPath = lambda : os.path.join(parentPath, getFolderName(projectName()))

    if os.path.exists(projectPath()):
        return (False, "%s has been existed." % getFolderName(projectName()))
    else:
        createProjectFolder(projectPath())
        createAnsibleFolder(projectPath(), deployConfig, serviceProject)
        serviceProject.serviceInterface != None and createMicroServiceAppFolder(projectPath(), projectName(), serviceProject, allServiceProjects)
        serviceProject.serviceInterface == None and serviceProject.getJson()["deployConfig"]["instanceType"] == 'frontApp' and createFrontAppFolder(projectPath(), projectName())
        
        return (True, projectPath())

def generateProxy(yamlGenModel):
    from jinja2 import Template
    def gen(projectFolder):
        createProjectFolder(projectFolder)
        
        def genLogsFolder():
            return createProjectFolder(os.path.join(projectFolder, "logs"))

        def genConfFolder():
            return createProjectFolder(os.path.join(projectFolder, "conf.d"))

        def getPort(service):
            return service.ports[0].split(":")[0] if isinstance(service.ports, list) else service.ports
        def getServices():
            return yamlGenModel.services \
                | where(lambda service: service.type in ["microService", "frontApp"]) \
                | select(lambda service: { "name": service.name, "port": getPort(service)}) \
                | as_list()
        
        def genConfig():
            return Template('''{% for server in servers %}upstream {{server.name}} {
  server {{server.name}}:{{server.port}};
  keepalive 2000;
}
{% endfor %} 

server {
  listen 80;
  server_name {{name}}
  client_max_body_size 1024M;

  {%for server in servers %}location /_api/{{server.name}}/ {
    proxy_pass http://{{server.name}}/;
    proxy_set_header Host $host:$server_port;
  }
{% endfor %}
}
 ''').render(servers = getServices())
        
        def genConfFile(configFolder):
            util.writeContent(os.path.join(configFolder, "app.conf"), \
                              genConfig())

        genLogsFolder()
        genConfFile(genConfFolder())
        
    gen(os.path.join(yamlGenModel.deployRootPath, yamlGenModel.proxyname))
    



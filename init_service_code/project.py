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

def getFolderName(projectName):
    return "_".join([x for x in re.split('''\s+''', projectName) if len(x.strip()) > 0])


def createProjectFolder(path):
    os.makedirs(path)

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

    (lambda content, (result, filePath):util.writeContent(filePath, content))\
        (RootGenerator(deployConfig.name, folderPath).gen(), createEmptyFile(folderPath, "run.yml"))



def createAppFolder(path,appName,  serviceProject, allServiceProjects):
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

    (lambda (result, path):util.writeContent(path, ProxyGenerator(serviceProject).gen()))(createEmptyFile(folderPath, "proxy.js"))
    
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
    

def generateCode(parentPath, serviceProject, allServiceProjects):
    deployConfig = serviceProject.deployConfig

    projectName = lambda : deployConfig.name
    projectPath = lambda : os.path.join(parentPath, getFolderName(projectName()))

    if os.path.exists(projectPath()):
        return (False, "%s has been existed." % getFolderName(projectName()))
    else:
        createProjectFolder(projectPath())
        createAnsibleFolder(projectPath(), deployConfig, serviceProject)
        serviceProject.serviceInterface != None and createAppFolder(projectPath(), projectName(), serviceProject, allServiceProjects)
        
        return (True, projectPath())



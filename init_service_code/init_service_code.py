#!/bin/python
from project import generateCode
import os
import getopt
import sys
import ansiblescript
import npm
from getParam import getParam, getServices
from models.serviceProject import ServiceProject
import env
import logging
from models.ansible.allGenerator import AllGenerator
import util

logging.basicConfig(filename="log.txt", filemode="w", level=logging.DEBUG)

def getparam(name, default = None):
    import getopt
    options, args = getopt.getopt(sys.argv[1:], "", ["isdebug="])
    return (lambda result: result[0][1] if len(result) > 0 else default) \
        ([opt for opt in util.log('debug', options, lambda n:{'param':n}) if opt[0] == '--%s' % name])

def main():
    def generateServices(rootPath, allServiceProjects):
        for serviceProject in allServiceProjects:

            #create the project folder
            status, projectPath = generateCode(rootPath, serviceProject, allServiceProjects)

            print('create the code at %s' % projectPath)

            if not status:
                return 1

    def generateRootAnsible(rootPath, allServiceProjects):
        (lambda content, re:util.writeContent(re[1], content))\
            (AllGenerator(rootPath, allServiceProjects).gen(), util.createEmptyFile(rootPath, "root.yml"))


    (lambda rootPath, allServiceProjects:(lambda x,y:x)(generateServices(rootPath, allServiceProjects), generateRootAnsible(rootPath, allServiceProjects)))\
        (env.runningPath(), list(map(lambda n:ServiceProject(n), getServices())))

    from models.ansible.yamlgen import genRoot, convertToModel, ConvertOption
    (lambda isDebug:genRoot(env.runningPath(), convertToModel(getServices(), ConvertOption(isDebug = getparam('isdebug', 'true').lower() == 'true', rootFolder = env.runningPath()))))(True)
    
    return 0


if __name__ == '__main__':
    # python main.py
    # the md.config should be the running path
    main()

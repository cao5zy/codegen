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
    

    
    return 0


if __name__ == '__main__':
    # python main.py
    # the md.config should be the running path
    main()

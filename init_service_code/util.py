#! /bin/python
import os
import shutil
from jinja2 import Template
import sys

def createFolder(folderName, parentPath = None):
    p = folderName if parentPath == None else os.path.join(parentPath, folderName)
    
    if os.path.exists(p):
        shutil.rmtree(p)
    
    os.makedirs(p)

def removeFolder(folderName):

    if os.path.exists(folderName):
        shutil.rmtree(folderName)

def readContent(path):
    with open(path, 'r') as file:
        return file.read()

def writeContent(path, content):
#    print('content:%s' % content)
    if not content: return
    with open(path, 'w') as file:
        file.write(content)

def applyTemplate(templatePath, targetPath, dataObj):
    template = Template(readContent(templatePath))
    writeContent(targetPath, template.render(dataObj))

def getTemplatePath(appPath, filename):
    print('getTemplatePath:appPath:%s' % appPath)
    return os.path.join(appPath, 'templates', '.'.join([filename, 'template']))

def createSubFolder(parentPath, folderName):

    subFolderPath = lambda : os.path.join(parentPath, folderName)

    if os.path.exists(subFolderPath()):
        return (False, "%s has been existed." % folderName)
    else:
        os.makedirs(subFolderPath())
        return (True, subFolderPath())

def createEmptyFile(parentPath, fileName):
    filePath = os.path.join(parentPath, fileName)
    with open(filePath, 'w') as f:
        return (True, filePath)


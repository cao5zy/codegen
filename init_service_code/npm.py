import os
import util
from Runner import Run
import demjson
import sys

def install(folderPath, name):
    '''folderPath: the path for the project
name: the name of the project
'''
    createPackagefile(folderPath, name)
#    installpackageByConfig(folderPath, getPackageNames(os.path.join(sys.path[0], 'npm.install.json')))

def createPackagefile(folderPath, name):
    util.applyTemplate(os.path.join(sys.path[0], 'templates/package.json.template'), os.path.join(folderPath, 'package.json'), { "name": name })

def getPackageNames(filename):
    data = demjson.decode_file(filename)
    return data
    

def installpackageByConfig(folderPath, packageNames):
    cmds = []
#    print('installpackageByConfig: folderpath %s' % folderPath)
    cmds.append('cd %s' % folderPath);
    for el in packageNames:
        cmds.append('npm install %s %s' %(el["name"], el["option"]))

    Run.command(';'.join(cmds))

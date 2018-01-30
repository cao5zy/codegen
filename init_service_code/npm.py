import os
import util
import shellrun
import demjson
import sys

def install(folderPath, name):
    '''folderPath: the path for the project
name: the name of the project
'''
    createPackagefile(folderPath, name, getPackageNames(os.path.join(sys.path[0], 'npm.install.json')))
#    installpackageByConfig(folderPath, getPackageNames(os.path.join(sys.path[0], 'npm.install.json')))

def createPackagefile(folderPath, name, packageList):
    util.applyTemplate(os.path.join(sys.path[0], 'templates/package.json.template'), os.path.join(folderPath, 'package.json'), { "name": name, "dependencies": packageList })

def getPackageNames(filename):
    from functional import seq
    return (seq(demjson.decode_file(filename))
        .map(lambda n: n["name"].split("@"))
            .map(lambda n: [ '"%s"' % n[0], '"%s"' % n[1]])
            .map(lambda n: ":".join(n))
            .to_list()
    )

def installpackageByConfig(folderPath, packageNames):
    cmds = []
#    print('installpackageByConfig: folderpath %s' % folderPath)
    cmds.append('cd %s' % folderPath);
    for el in packageNames:
        cmds.append('npm install %s %s' %(el["name"], el["option"]))

    shellrun.run(';'.join(cmds))


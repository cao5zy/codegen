from Runner import Run
import unittest
import util
import project
from assertpy import assert_that
import os
import time
import ansiblescript
import pdb
import npm
_folderName = 'unit_test_for_create_project_folder'
class Create_code_test(unittest.TestCase):
    def setUp(self):
        util.createFolder(_folderName)
    def tearDown(self):
        util.removeFolder(_folderName)

    def testGetFolderName(self):
        assert_that(project.getFolderName("project one")).is_equal_to("project_one")
        assert_that(project.getFolderName("projectOne")).is_equal_to("projectOne")
        assert_that(project.getFolderName(" project one ")).is_equal_to("project_one")
        
        
    def testCreateSubFolder(self):
        parentPath = "test_create_sub_folder"
        projectName = "project1"
        unittestsFolderName = "tests"


        try:
             Run.command("mkdir %s" % parentPath)
             result, unittestsFolderPath = project.createSubFolder(parentPath, unittestsFolderName)

             assert_that(os.path.exists(unittestsFolderPath)).is_equal_to(True)
        except:
            assert_that(True).is_equal_to(False)

        finally:
            Run.command("rm %s -rf" % parentPath)

    def testCreateEmptyFile(self):
        parentPath = _folderName
        fileName = "test1.yml"
        
        result, filePath = project.createEmptyFile(parentPath, fileName)

        assert_that(result).is_equal_to(True)
        assert_that(os.path.exists(os.path.join(parentPath, fileName))).is_equal_to(True)
        
    def testAddBase(self):
        result, filePath = project.createEmptyFile(_folderName, "test.yml")

        ansiblescript.addBase(filePath)

        content = ''
        with open(filePath, 'r') as f:
            content = f.read()
            
        assert_that(content).contains('---')
        assert_that(content).contains('name:')
        assert_that(content).contains('become: true')
        assert_that(content).contains('hosts: localhost')
        assert_that(content).contains('become_method: sudo')
        assert_that(content).contains('tasks:')


    def testAddUnitTests(self):
        result, filePath = project.createEmptyFile(_folderName, "test.yml")

        ansiblescript.addBase(filePath)
        ansiblescript.addUnitTests(filePath)
        
        content = ''
        with open(filePath, 'r') as f:
            content = f.read()

        assert_that(content).contains('  - name')
        assert_that(content).contains('    shell')
        

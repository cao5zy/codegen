from getParam import getServices
from models.serviceProject import ServiceProject
from models.code.logModuleGenerator import LogModuleGenerator
from assertpy import assert_that

def test_logModuleGenerator():
    serviceProjects = list(map(lambda n:ServiceProject(n), getServices()))
    testServiceProject = list(filter(lambda n:n.name == "Test_Project", serviceProjects))[0]
    content = LogModuleGenerator(testServiceProject).gen()

    assert_that(content).contains('''log4js.getLogger("%s");''' % "Test_Project")

    

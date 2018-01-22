from getParam import getServices
from models.serviceProject import ServiceProject
from models.code.configGenerator import ConfigGenerator
from assertpy import assert_that

def test_configGenerator():
    serviceProjects = list(map(lambda n:ServiceProject(n), getServices()))
    testServiceProject = list(filter(lambda n:n.name == "Test_Project", serviceProjects))[0]
    content = ConfigGenerator(testServiceProject, serviceProjects).gen()

    assert_that(content).contains('''"int_serviceHost": "http://int_service"''')
    assert_that(content).contains('''"int_servicePort": 8088''')
    assert_that(content).contains('''"port": 8089''')
    assert_that(content).contains('''"interval": 33''')
    assert_that(content).contains('''"timeout": 50''')
    

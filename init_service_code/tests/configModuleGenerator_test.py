from getParam import getServices
from models.code.configModuleGenerator import ConfigModuleGenerator
from models.serviceProject import ServiceProject
from assertpy import assert_that

def test_configModuleGenerator():
    serviceProjects = list(map(lambda n:ServiceProject(n), getServices()))
    testServiceProject = list(filter(lambda n:n.name == "Test_Project", serviceProjects))[0]
    content = ConfigModuleGenerator(testServiceProject, serviceProjects).gen()

    assert_that(content).contains('''int_serviceHost: config.get("int_serviceHost"),''')
    assert_that(content).contains('''int_servicePort: config.get("int_servicePort"),''')
    assert_that(content).contains('''port: config.get("port"),''')
    assert_that(content).contains('''interval: config.get("interval")''')
    assert_that(content).contains('''timeout: config.get("timeout")''')


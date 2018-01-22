import util
import demjson
from models.code.logConfigGenerator import LogConfigGenerator
from models.serviceProject import ServiceProject
from getParam import getServices
from assertpy import assert_that

def test_logConfigGenerator():
    serviceProjects = list(map(lambda n:ServiceProject(n), getServices()))
    testServiceProject = list(filter(lambda n:n.name == "Test_Project", serviceProjects))[0]
    content = LogConfigGenerator(serviceProjects, testServiceProject.dependedServers).gen()

    assert_that(content).contains('''"host": "logsvr1"''')
    assert_that(content).contains('''"port": 8322''')
    

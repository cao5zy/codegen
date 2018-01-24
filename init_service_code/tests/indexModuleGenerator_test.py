from models.code.indexModuleGenerator import IndexModuleGenerator
from getParam import getServices
from models.serviceProject import ServiceProject
from assertpy import assert_that

def test_indexModuleGenerator():
    serviceProjects = list(map(lambda n:ServiceProject(n), getServices()))
    testServiceProject = list(filter(lambda n:n.name == "Test_Project", serviceProjects))[0]
    content = IndexModuleGenerator(testServiceProject, serviceProjects).gen()

    assert_that(content).contains("require('./Auth')")
    assert_that(content).contains("service.use(Auth);")
    assert_that(content).contains('service.listen({port: conf.port}')


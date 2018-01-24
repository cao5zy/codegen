from models.ansible.yamlgen import YamlGenModel
from assertpy import assert_that
import util
import easyrun

    
def genTestModel():
    genModel = YamlGenModel()
    genModel.services.append(YamlGenModel.Service(name = "ab"))
    genModel.services.append(YamlGenModel.Service(name = "cd"))
 
    return genModel
def YamlGenModel_test():
    genModel = genTestModel()
    assert_that(genModel.services[0].name).is_equal_to("ab")

def genRoleFolder_test():
    from models.ansible.yamlgen import genRoleFolder
    try:
        genModel = genTestModel()
        result = genRoleFolder(".", genModel)
        assert_that(easyrun.run("ls ab").retcode).is_equal_to(0)
        assert_that(easyrun.run("ls cd").retcode).is_equal_to(0)
    finally:
        easyrun.run("rm ab -rf")
        easyrun.run("rm cd -rf")


def BlockBuilder_test():
    from models.ansible.yamlgen import BlockBuilder
    
    builder = BlockBuilder("service1", "docker_container")
    result = builder.add("name", "service1").add("ports", [8080]).gen()
    path = "./temp.yaml"
    util.writeContent(path, "---\n" + result)

    try:
        result = easyrun.run('yamllint %s' % path)
        assert_that(result.retcode).is_equal_to(0)
        print(result.output)
    finally:
        easyrun.run('rm %s' % path)
    
    

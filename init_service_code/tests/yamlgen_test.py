from models.ansible.yamlgen import YamlGenModel
from assertpy import assert_that
import util
import easyrun
from Runner import Run
    
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
        assert_that(bool(Run.command("ls ab"))).is_equal_to(True)
        assert_that(bool(Run.command("ls cd"))).is_equal_to(True)
    finally:
        Run.command("rm ab -rf")
        Run.command("rm cd -rf")


def BlockBuilder_test():
    from models.ansible.yamlgen import BlockBuilder
    
    builder = BlockBuilder("service1", "docker_container")
    result = builder.add("name", "service1").add("ports", [8080]).gen()
    path = "./temp.yaml"
    util.writeContent(path, "---\n" + result)

    try:
        result = Run.command('yamllint %s' % path)
        assert_that(bool(result)).is_equal_to(True)
        print(result.stdout)
    finally:
        Run.command('rm %s' % path)

def genTaskMain_test():
    parentPath = "./"
    from models.ansible.yamlgen import genTaskMain

    filePath = genTaskMain(parentPath, YamlGenModel.Service(name="test_service"))

    try:
        result = Run.command('yamllint %s' % filePath)
        assert_that(bool(result)).is_equal_to(True)
        print(result.stdout)
    finally:
        pass
    

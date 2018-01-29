from models.ansible.yamlgen import YamlGenModel
from assertpy import assert_that
import util
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
    import shellrun
    
    builder = BlockBuilder().addTitle("name", "deploy service1").add("docker_container")
    result = builder.add("name", "service1", 2).add("ports", [8080], 2).gen()
    path = "./temp.yaml"
    util.writeContent(path, "---\n" + result)

    try:
        result = shellrun.run('yamllint %s' % path)
        assert_that(result.retcode).is_equal_to(0)
        print(result.output)
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
        assert_that(bool(Run.command('rm %s' % filePath))).is_equal_to(True)
    
def convertToModel_test():
    import demjson
    from models.ansible.yamlgen import convertToModel
    json = demjson.decode("[{'deployConfig': {'image_tag': '1.0', 'volume': '/working', 'description': null, 'entrypoint': 'node index.js', '_id': '5a446071f521b50001971f98', 'image': 'alancao/node_server_image', 'port': 8082, 'name': 'edgesvr2', 'restart': false, 'instanceType': 'microService', 'target': null, 'volumes': [{'container': '/working'}], 'awsSetting': null, 'recreate': false}, 'dependedServers':[{'name': 'interface_service'}]}]")
    result = convertToModel(json, "./")

    assert_that(result.services[0].name).is_equal_to("edgesvr2")
    assert_that(len(result.services[0].volumes)).is_equal_to(1)
    assert_that(result.relations[0].name).is_equal_to("edgesvr2")
    assert_that(result.relations[0].depend).is_equal_to("interface_service")
    
def ConfigBuilder_test():
    from models.ansible.yamlgen import ConfigBuilder

    result = ConfigBuilder() \
    .addSection("defaults") \
    .addKeyValue("inventory", "hosts") \
    .gen()
    assert_that(result).contains("inventory=hosts")


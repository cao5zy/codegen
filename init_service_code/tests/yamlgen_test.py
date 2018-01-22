from models.ansible.yamlgen import YamlGenModel
from assertpy import assert_that

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
    import easyrun
    try:
        genModel = genTestModel()
        result = genRoleFolder(".", genModel)
        assert_that(easyrun.run("ls ab").retcode).is_equal_to(0)
        assert_that(easyrun.run("ls cd").retcode).is_equal_to(0)
    finally:
        easyrun.run("rm ab -rf")
        easyrun.run("rm cd -rf")


    

from models.ansible.yamlgen import YamlGenModel
from assertpy import assert_that

def YamlGenModel_test():
    genModel = YamlGenModel()
    genModel.services.append(YamlGenModel.Service(name = "ab"))
    assert_that(genModel.services[0].name).is_equal_to("ab")

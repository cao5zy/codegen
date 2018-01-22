from models.ansible.dependencyGenerator import DependencyGenerator
import demjson
from assertpy import assert_that

def test_dependencyGenerator():
    result = DependencyGenerator(demjson.decode('''  {
    dependedServers:[
      {
        name: "interface_service",
	localName: "int_service",
	type: "service"
      },
      {
        name: "logsvr",
	localName: "logsvr1",
	type: "logserver"
      }
      ]
  }''')).gen()

    print(result)
    assert_that(result).contains('- include: ../../interface_service/ansible/deploy.yml')
    assert_that(result).contains('- include: ../../logsvr/ansible/deploy.yml')


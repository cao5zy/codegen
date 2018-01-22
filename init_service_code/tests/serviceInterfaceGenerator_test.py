from models.code.serviceInterfaceGenerator import ServiceInterfaceGenerator
from models.serviceInterface import ServiceInterface
import demjson
from assertpy import assert_that

def test_ServiceInterfaceGenerator():
    content = ServiceInterfaceGenerator(ServiceInterface(demjson.decode('''{
      name: "Auth",
      methods:[{
        name: "authenticate",
	params:[{
	  name: "username",
	  type: "string",
	  isUrlFilter: "True",
          defaultVal:"alan"
	},
	{
	  name: "password",
	  type: "string"
	}]
      }]
    }'''))).gen()

    assert_that(content).contains("function Auth")
    assert_that(content).contains('this.add({ username:"alan"  }, (msg, respond)=>{')
    assert_that(content).contains('this.add({test:"hello-world"}, (msg, respond)=>{')

    
    
    

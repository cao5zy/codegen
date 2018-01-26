#!bin/python
from getParam import Param
from assertpy import assert_that
import shellrun

def test_getParam():
    configfile = '''{
    "logServer": \\"logsvr\\",
    "logServerPort": 3232,
    "services":[{
      deployConfig:{
        "name":\\"Test Project\\"
      }
    }]
} '''
    testConfigFile = "test_config.json"
    print('test_getParam')
    shellrun.run('echo "%s" >> %s' % (configfile, testConfigFile))

    try:
        param = Param(testConfigFile)
        assert_that(param.services[0]["deployConfig"]["name"]).is_equal_to('Test Project')
        assert_that(param.getParam('logServer')).is_equal_to('logsvr')
        assert_that(param.getParam('logServerPort')).is_equal_to(3232)

    finally:
        shellrun.run('rm %s' % testConfigFile)
    

    
    

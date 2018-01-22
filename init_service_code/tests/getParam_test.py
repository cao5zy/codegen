#!bin/python
from getParam import Param
import easyrun
from assertpy import assert_that

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
    easyrun.run('echo "%s" >> %s' % (configfile, testConfigFile))

    try:
        param = Param(testConfigFile)
        assert_that(param.services[0]["deployConfig"]["name"]).is_equal_to('Test Project')
        assert_that(param.getParam('logServer')).is_equal_to('logsvr')
        assert_that(param.getParam('logServerPort')).is_equal_to(3232)

    finally:
        easyrun.run('rm %s' % testConfigFile)
    

    
    

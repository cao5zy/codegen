from models.ansible.deployConfigGenerator import DeployConfigGenerator
import ansiblescript
import easyrun
import os
from models.deployConfig import DeployConfig
from assertpy import assert_that, contents_of
import demjson

serviceProjectJson = demjson.decode('''{
    param: {
      deploy_path: "Test_Project_Deploy_Path"
    },
    port: {
      host: 8322,
      container: 8322
    },
    deployConfig:{
      name: "Test_Project" ,
      image: "md-app",
      image_tag: "1.0",
      volumes: [{container: "/app"}],
      restart: "yes",
      recreate: "yes",
      state: "started",
      entrypoint: "node index.js"
    },
    dependedServers:[
      {
        name: "interface_service",
	localName: "int_service",
	type: "service"
      },
      {
        name: "logsvr1",
	localName: "logsvr",
	type: "logserver"
      },
      {
        name: "interface_db",
	localName: "int_db",
	type: "db"
      }
    ]
    
  }''')

serviceProjectJson1 = demjson.decode('''{
    param: {
      deploy_path: "Test_Project_Deploy_Path"
    },
    port: {
      host: 8322,
      container: 8322
    },
    deployConfig:{
      name: "Test_Project" ,
      image: "md-app",
      image_tag: "1.0",
      volumes: [{host: "{{ deploy_path }}", container: "/app"}],
      restart: "yes",
      recreate: "yes",
      state: "started",
      entrypoint: "node index.js"
    },
    interface:{
      name: "test interface"
    }
    
  }''')
def test_CopyConfigInDeployScript():
    deployConfig = DeployConfig(serviceProjectJson1)

    content = DeployConfigGenerator(deployConfig, serviceProjectJson1).gen()
    assert_that(content).contains('''name: copy Test_Project to deployment''')
    assert_that(content).contains('''src: "{{ Test_Project_source }}"''')
    assert_that(content).contains('''dest: "{{ Test_Project_dest }}"''')


def test_addDeployScript():
    deployConfig = DeployConfig(serviceProjectJson)

    content = DeployConfigGenerator(deployConfig, serviceProjectJson).gen()
    assert_that(content).contains('''name: "Test_Project"''')
    assert_that(content).contains('''image: "md-app:1.0"''')
    assert_that(content).contains('''volumes:''')
    assert_that(content).contains('''- "{{ Test_Project_dest }}:/app"''')
    assert_that(content).contains('''ports:''')
    assert_that(content).contains('''- "8322:8322"''')
    assert_that(content).contains('''links:''')
    assert_that(content).contains('''- "logsvr1:logsvr"''')
    assert_that(content).contains('''- "interface_db:int_db"''')
    assert_that(content).contains('''restart: "yes"''')
    assert_that(content).contains('''recreate: "yes"''')
    assert_that(content).contains('''state: "started"''')
    assert_that(content).contains('''entrypoint: "node index.js"''')


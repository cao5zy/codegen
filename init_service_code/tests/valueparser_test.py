import valueparser
import demjson
from assertpy import assert_that

def test_getFieldOfParam():
    json = demjson.decode('''{
    param: {
      deploy_path: "Test_Project_Deploy_Path"
    },
    name: "Test_Project" ,
    image: "md-app",
    image_tag: "1.0",
    volumes: [{from: "{{ deploy_path }}", to: "/app"}],
    ports: [ {host: 8322, container: 8322}],
    links: [ {host: "logsvr", container: "logsvr" },
    {host: "interface-service", container: "interface-service"}],
    restart: "yes",
    recreate: "yes",
    state: "started",
    entrypoint: "node index.js"
  }''')
    
    assert_that(valueparser.getFieldOfParam(json, "{{ deploy_path }}")).is_equal_to("{{ Test_Project_Deploy_Path }}")

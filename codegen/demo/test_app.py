from codegen import run
from nose import with_setup
from assertpy import assert_that
import os
import logging
from codegenhelper import test_root, init_test_folder, remove_test_folder, put_file

logging.basicConfig(level = logging.DEBUG)

def setup_folder():
    init_test_folder()

    put_file("datafile", test_root(), '''{
    deployConfig: {instanceName: "tourist2"}
} ''')
    
@with_setup(setup_folder, remove_test_folder)
def test_run():
    url = "http://104.46.103.208:9008"
    username = "alan1"
    password = "123"
    root = test_root()
    project_name = "test1"
    template_url = "git@github.com:cao5zy/nodejs_microservice_seneca_template.git"
    template_tag = "v0.0.2"
    run(root, url, project_name, template_url, template_tag, username, password)

    assert_that(os.path.join(test_root(), ".template",  "nodejs_microservice_seneca_template")).exists()
    assert_that(os.path.join(test_root(), "tourist", "src",  "app.js")).exists()
    
    assert_that(os.path.join(test_root(), "customers", "src",  "app.js")).exists()
    
    assert_that(os.path.join(test_root(), "inventory", "src",  "app.js")).exists()
    assert_that(os.path.join(test_root(), "inventory", "src",  "config", "log4js.json")).exists()
    
    
@with_setup(setup_folder, remove_test_folder)    
def test_run_data_str():
    root = test_root()
    template_url = "git@github.com:cao5zy/nodejs_microservice_seneca_template.git"
    template_tag = "v0.0.2"

    run(root, "", "", template_url, template_tag, jsonstr = '''{ "deployConfig":{"instanceName": "test1"}}''')

    assert_that(os.path.join(test_root(), "test1", "src",  "app.js")).exists()

@with_setup(setup_folder, remove_test_folder)    
def test_run_data_file():
    root = test_root()
    template_url = "git@github.com:cao5zy/nodejs_microservice_seneca_template.git"
    template_tag = "v0.0.2"

    run(root, "", "", template_url, template_tag, datafile = os.path.join(test_root(), "datafile"))

    assert_that(os.path.join(test_root(), "tourist2", "src",  "app.js")).exists()

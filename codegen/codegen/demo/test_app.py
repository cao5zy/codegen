from codegen import run
from nose import with_setup
from assertpy import assert_that
import os
import logging
from codegenhelper import test_root, init_test_folder, remove_test_folder

logging.basicConfig(level = logging.DEBUG)

def setup_folder():
    init_test_folder()
    
    
@with_setup(setup_folder, remove_test_folder)
def test_run():
    url = "http://104.46.103.208:9008"
    username = "alan1"
    password = "123"
    root = test_root()
    project_name = "test1"
    template_url = "git@github.com:cao5zy/nodejs_microservice_seneca_template.git"
    template_tag = "0.0.1"
    run(root, url, project_name, template_url, template_tag, username, password)

    assert_that(os.path.join(test_root(), ".template", "nodejs_microservice_seneca_template")).exists()

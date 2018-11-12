from codegen import run
from assertpy import assert_that
import os

def test_run():
    url = "http://104.46.103.208:9008"
    username = "alan1"
    password = "123"
    root = "./test"
    project_name = "test1"
    run(root, url, project_name, username, password)

    assert_that(os.path.exists(root)).is_true()

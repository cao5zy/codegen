from codegen import run
from assertpy import assert_that
import os

def test_run():
    url = "http://130.175.64.9:9008/_api/interface_service/interface_service"
    username = "alan1"
    password = "123"
    root = "./test"
    run(root, url, username, password)

    assert_that(os.path.exists(root)).is_true()

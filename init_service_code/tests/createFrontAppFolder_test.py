from project import createFrontAppFolder
from assertpy import assert_that, contents_of
import shellrun
import os

def test_createFrontAppFolder():
    appName = "test_front_app"

    try:
        path = createFrontAppFolder("./", appName)
        assert_that(os.path.join(path, "package.json")).exists()
        content = contents_of(os.path.join(path, "package.json"))
        assert_that(content).contains('''"name": "test_front_app"''')
    finally:
        shellrun.run("rm {name} -rf".format(name = appName))

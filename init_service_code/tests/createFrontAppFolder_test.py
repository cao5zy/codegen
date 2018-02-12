from project import createFrontAppFolder
from assertpy import assert_that
import shellrun
import os

def test_createFrontAppFolder():
    appName = "test_front_app"

    try:
        path = createFrontAppFolder("./", appName, None)
        assert_that(os.path.join(path, "package.json")).exists()
    finally:
        shellrun.run("rm {name} -rf".format(name = appName))

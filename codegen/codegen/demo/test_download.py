from codegen.download import getJson
from assertpy import assert_that

def test_download():
    url="http://104.46.103.208:9008"

    assert_that(getJson(url, "test1", 'alan1', '123')[0]).contains('deployConfig')


from codegen.download import getJson
from assertpy import assert_that

def test_download():
    url="http://http://130.175.64.9:9008/_api/interface_service"

    assert_that(getJson(url)).contains('name')


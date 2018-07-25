from codegen import Download
from assertpy import assert_that

def test_download():
    url="http://http://130.175.64.9:9008/_api/interface_service"
    download = Download()
    download.getUserName()
    download.getPwd()
    assert_that(download.getJson(url)).contins('name')

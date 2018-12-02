from ..download import get_login_url, getJson
from assertpy import assert_that

def test_get_login_url():
    url = "http://130.123.2.5:8990/_api/interface_service/interface_service"
    
    assert_that(get_login_url(url)).is_equal_to("http://130.123.2.5:8990/auth/login")


def test_download():
    url="http://104.46.103.208:9008"

    assert_that(getJson(url, "test1", 'alan1', '123')[0]).contains('deployConfig')



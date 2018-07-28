from codegen.download import get_login_url
from assertpy import assert_that

def test_get_login_url():
    url = "http://130.123.2.5:8990/_api/interface_service/interface_service"
    
    assert_that(get_login_url(url)).is_equal_to("http://130.123.2.5:8990/auth/login")

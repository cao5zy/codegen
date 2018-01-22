from assertpy import assert_that
from models.nameRule import NameRule

def test_nameRule():
    rule = NameRule()

    assert_that(rule.isValid("test service")).is_equal_to(False)
    assert_that(rule.isValid("test-service")).is_equal_to(False)
    assert_that(rule.isValid("testService")).is_equal_to(True)
    assert_that(rule.isValid(" testService ")).is_equal_to(False)
    assert_that(rule.isValid("test_service")).is_equal_to(True)
    assert_that(rule.isValid("testservice1")).is_equal_to(True)
    assert_that(rule.isValid("1testservice")).is_equal_to(False)
    assert_that(rule.isValid("test@service")).is_equal_to(False)

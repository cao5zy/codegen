import re

class NameRule:
    def __init__(self):
        self.__rule = '''^(?!\d)\w+[^_]$'''

    @property
    def rule(self):
        return self.__rule

    def isValid(self, val):
        return re.match(self.__rule, val) != None

def validateName(func):
    def __decorator(obj):
        result = func(obj)
        if not NameRule().isValid(result):
            raise ValueError("name rule is broken: %s" % result)
        return result

    return __decorator

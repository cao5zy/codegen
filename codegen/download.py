from urllib.parse import urlparse
from codegenhelper import debug
import requests
import urllib

def get_input(name):
    result = input("please input {}:".format(name))
    if not result:
        raise Exception("no {} is supplied".format(name))
    return result

def get_login_url(url):
    return (lambda result:"{scheme}://{netloc}/auth/login".format(scheme = debug(result, "result").scheme, netloc = result.netloc))(urlparse(url))

def getToken(login_url, userName, pwd):
    def get_token(username, password):
        return (lambda result:\
                result.content.decode(result.encoding))\
                (requests.post(login_url, json={"name": username, "pwd": password}))
            

    return get_token(userName or get_input("username"), pwd or get_input("pwd"))

def get_json(url, token):
    pass

def getJson(url, userName=None, pwd=None):
    return get_json(url, getToken(get_login_url(url), userName, pwd))

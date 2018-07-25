from urllib.parse import urlparse
from codegenhelper import debug

def get_input(name):
    result = input("please input {}:".format(name))
    if not result:
        raise Exception("no {} is supplied".format(name))
    return result

def get_login_url(url):
    return (lambda result:"{scheme}://{netloc}/auth".format(scheme = result.scheme, netloc = result.netloc))(urlparse(url))

def getToken(login_url, userName, pwd):
    def get_token(username, password):
        pass

    return get_token(userName or get_input("username"), pwd or get_input("pwd"))

def get_json(url, token):
    pass

def getJson(url, userName=None, pwd=None):
    return get_json(url, getToken(get_login_url(url), userName, pwd))

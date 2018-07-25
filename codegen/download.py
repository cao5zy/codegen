from urllib.parse import urlparse
from codegenhelper import debug

def get_user_name():
    pass

def get_pwd():
    pass

def get_login_url(url):
    return (lambda result:"{scheme}://{netloc}/auth".format(scheme = result.scheme, netloc = result.netloc))(urlparse(url))

def getToken(login_url, userName, pwd):
    def get_token(username, passwork):
        pass

    return get_token(userName or get_user_name(), pwd or get_pwd())

def get_json(url, token):
    pass

def getJson(url, userName=None, pwd=None):
    return get_json(url, getToken(get_login_url(url), userName, pwd))

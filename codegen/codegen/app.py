import nodejs_codegen 
from .download import getJson
from codegenhelper import put_folder, debug

def run(root, url, username = None, password = None):
    (lambda folder_path: \
     [nodejs_codegen.run(debug(app_data, "app_data"), \
          put_folder(app_data["deployConfig"]["instanceName"], folder_path)) for app_data in getJson(url, username, password) ])(put_folder(root))

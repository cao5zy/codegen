import nodejs_codegen 
from .download import getJson
from codegenhelper import put_folder, debug

def run(root, url, username = None, password = None):
    def gen_code(app_data, project_folder):
        nodejs_codegen.run(app_data, project_folder)
    
    (lambda folder_path: \
     [gen_code(debug(app_data, "app_data"), \
          put_folder(app_data["deployConfig"]["instanceName"], folder_path)) for app_data in getJson(url, username, password) ])(put_folder(root))

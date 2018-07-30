from nodejs_codegen import gen
from .download import getJson
from codegenhelper import put_folder, debug

def run(root, url, username = None, password = None):
    (lambda folder_path: \
     [gen("app", \
          get_app(debug(app_data, "app_data")), \
          put_folder(app_data["deployConfig"]["instanceName"], folder_path)) for app_data in getJson(url, username, password) ])(put_folder(root))

def get_app(json):
    return {
        "name": json["serviceInterface"]["name"],
        "methods": list(map(lambda method:method["name"], json["serviceInterface"]["methods"])),
        "dep_services": list(map(lambda service: service["name"], json["dependedServers"])) if "dependedServers" in json else None
    }

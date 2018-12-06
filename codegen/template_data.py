import os
import demjson
from  deep_mapper import process_mapping

class TemplateData:
    def __init__(self):
        def func(project_name):
            def get_project_name(jsonData, template_path):
                def map_project_name(project_name_map_file):
                    if not os.path.exists(project_name_map_file):
                        raise ValueError("the map file is not available--%s" % project_name_map_file)

                    return process_mapping(jsonData, demjson.decode_file(project_name_map_file), "/")[project_name]

                return jsonData[project_name] if project_name in jsonData else map_project_name(os.path.join(template_path, ".mapper"))

            self.get_project_name = get_project_name

        func("project_name")

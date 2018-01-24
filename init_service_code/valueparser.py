#! /bin/python

def getFieldOfParam(json, value):
    def getparam():
        try:
            return json["param"] if "param" in json.keys() else None
        except Exception as e:
            raise ValueError("param not defined in the json")
            
    
    def isParam():
        return True if isinstance(value, str) or isinstance(value, unicode) and len(value) >= 4 and value[0:2] == "{{" and value[len(value)-2:] == "}}" else False
    def getFieldName():
        return value.replace("{{", "").replace("}}", "").strip()
        
    return value if not isParam() else "{{ %s }}" % getparam()[getFieldName()]

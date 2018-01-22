#! /bin/python
from valueparser import getFieldOfParam
from .dependedServer import getDependedServers
from models.nameRule import validateName
import logging

class DeployConfig:
    def __init__(self, json):
        logging.debug({"deployConfig": json["deployConfig"]})
        logging.debug({"root": json})
        self.json = json["deployConfig"]
        self.root = json

    @property
    @validateName
    def name(self):
        return self.json["name"]
    @property
    def image(self):
        return "%s:%s" % (self.json["image"], self.json["image_tag"] if "image_tag" in self.json.keys() else "latest")

    @property
    def volumes(self):
        return None if not "volumes" in self.json.keys() else self.json["volumes"]

    @property
    def port(self):
        return (lambda name:None if not name in self.root.keys() else \
                { "host": self.root[name]["host"], "container": self.root[name]["container"]})("port")

    @property
    def links(self):
        return None if getDependedServers(self.root) == None else map(lambda n: { "host": n.name, "container":n.localName}, getDependedServers(self.root))

    def getNullableValue(self, keyName):
        return None if not keyName in self.json.keys() else self.json[keyName]

    @property
    def restart(self):
        return self.getNullableValue("restart")

    @property
    def recreate(self):
        return self.getNullableValue("recreate")

    @property
    def state(self):
        return self.getNullableValue("state")

    @property
    def entrypoint(self):
        return self.getNullableValue("entrypoint")

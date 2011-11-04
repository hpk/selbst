import requests
import json


class ThermostatClient(object):
    def __init__(self, ip_addr):
        self.ip_addr = ip_addr

    @property
    def base(self):
        return "http://%s" % self.ip_addr

    def send(self, path, data):
        return json.loads(requests.post(self.base+path, json.dumps(data)).content)

    def get(self, path):
        return json.loads(requests.get(self.base+path).content)

    

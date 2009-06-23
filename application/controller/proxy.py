#!-*- conding:utf-8 -*-
from gaeo.controller import BaseController

import os, yaml
from libs.amazon import ProductAdvertising

class ProxyController(BaseController):
    def proxy(self):
        xml_file = os.path.join( os.path.dirname(__file__), '../../amazon-auth-proxy.yaml' )
        conf = yaml.load( open(xml_file) )
        pa = ProductAdvertising(conf, self.params)
        self.render(
            xml=pa.send_request()
        )

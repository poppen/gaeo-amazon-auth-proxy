#!-*- conding:utf-8 -*-
from gaeo.controller import BaseController

import os, yaml
from libs.amazon import ProductAdvertising

class ProxyController(BaseController):
    def _is_ua_proxy(self):
        if 'rpaproxy' in self.request.headers['User-Agent']:
            return True
        else:
            return False

    def proxy(self):
        xml_file = os.path.join( os.path.dirname(__file__), '../../amazon-auth-proxy.yaml' )
        conf = yaml.load( open(xml_file) )
        pa = ProductAdvertising(conf, self.params)

        if conf['use_redirect'] and self._is_ua_proxy():
            self.redirect( pa.build_url() )
        else:
            self.render(
                xml=pa.send_request()
            )

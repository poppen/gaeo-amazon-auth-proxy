# -*- coding: utf-8 -*-
import urllib, urllib2, hmac, hashlib, base64, urlparse
from datetime import datetime

class ProductAdvertising:

    def __init__(self, conf, params):
        self.conf = conf
        self.options = {}
        for key in params:
            if key == 'AWSAccessKeyId':
                self.options[key] = self.conf['access_key']
            elif key == 'controller' or key == 'action':
                pass
            else:
                self.options[key] = params[key]
         
        if not self.options.has_key('AssociateTag'):
            self.options['AssociateTag'] = self.conf['default_aid']
        if not self.options.has_key('Timestamp'):
            self.options['Timestamp'] = datetime.utcnow().isoformat()

    def send_request(self):
        payload = ""
        for v in sorted( self.options.items() ):
            payload += '&%s=%s' % (v[0], urllib.quote(str(v[1])))
        payload = payload[1:]

        uri = urlparse.urlparse( self.conf['entry_point'] )[1:]
        strings = ['GET', uri[0], uri[1], payload]

        digest = hmac.new( self.conf['secret_key'], '\n'.join(strings), hashlib.sha256 ).digest()
        signature = base64.b64encode(digest)

        url = "http://%s%s?%s&Signature=%s" % (uri[0], uri[1], payload, urllib.quote_plus(signature))
        return urllib2.urlopen(url).read()

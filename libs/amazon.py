# -*- coding: utf-8 -*-
import urllib, urllib2, hmac, hashlib, base64, urlparse
from datetime import datetime

class ProductAdvertising:

    def __init__(self, conf, params):
        self.conf = conf
        self.options = {}
        self.entry_points = {
                'us':'http://webservices.amazon.com/onca/xml',
                'jp':'http://webservices.amazon.co.jp/onca/xml',
                'fr':'http://webservices.amazon.fr/onca/xml',
                'uk':'http://webservices.amazon.co.uk/onca/xml',
                'de':'http://webservices.amazon.de/onca/xml',
                'ca':'http://webservices.amazon.ca/onca/xml'
        }
        self.xslt_entry_points = {
                'us':'http://xml-us.amznxslt.com/onca/xml',
                'jp':'http://xml-jp.amznxslt.com/onca/xml',
                'fr':'http://xml-fr.amznxslt.com/onca/xml',
                'uk':'http://xml-uk.amznxslt.com/onca/xml',
                'de':'http://xml-de.amznxslt.com/onca/xml',
                'ca':'http://xml-ca.amznxslt.com/onca/xml'
        }
        self.countrycode = ''

        for key in params:
            if key == 'AWSAccessKeyId' or key == 'SubscriptionId':
                self.options[key] = self.conf['access_key']
            elif key == 'countrycode':
                self.countrycode = params['countrycode']
            elif key == 'Timestamp' or key == 'controller' or key == 'action':
                pass
            else:
                self.options[key] = params[key]

        self.options['Timestamp'] = datetime.utcnow().isoformat()

    def get_entry_point(self, countrycode = ''):
        if self.options.has_key('Style'):
            if not countrycode:
                return self.conf['default_xslt_entry_point']
            elif self.xslt_entry_points.has_key(countrycode):
                return self.xslt_entry_points[countrycode]
            else:
                return self.conf['default_xslt_entry_point']
        else:
            if not countrycode:
                return self.conf['default_entry_point']
            elif self.entry_points.has_key(countrycode):
                return self.entry_points[countrycode]
            else:
                return self.conf['default_entry_point']

    def get_aid(self, countrycode = ''):
        if not countrycode:
            return self.conf['default_aid']
        else:
            try:
                if self.conf['aids'].has_key(countrycode):
                    return self.conf['aids'][countrycode]
            except KeyError:
                return self.conf['default_aid']

    def build_url(self):
        if not self.options.has_key('AssociateTag'):
            self.options['AssociateTag'] = self.get_aid(self.countrycode)

        payload = ""
        for v in sorted( self.options.items() ):
            payload += '&%s=%s' % (v[0], urllib.quote( unicode(v[1]).encode('utf-8'),safe='~' ))
        payload = payload[1:]

        uri = urlparse.urlparse( self.get_entry_point(self.countrycode) )[1:]
        strings = ['GET', uri[0], uri[1], payload]

        digest = hmac.new( self.conf['secret_key'], '\n'.join(strings), hashlib.sha256 ).digest()
        signature = base64.b64encode(digest)

        url = "http://%s%s?%s&Signature=%s" % (uri[0], uri[1], payload, urllib.quote(signature,safe='~'))
        return url

    def send_request(self):
        url = self.build_url()
        return urllib2.urlopen(url).read()

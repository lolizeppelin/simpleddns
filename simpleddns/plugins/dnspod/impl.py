import requests
import json
import urllib
from oslocfg import cfg
from simpleddns.plugins import notifyBase
from simpleddns.plugins.dnspod import config

CONF = cfg.CONF


config.register_opts()


class notifyHelper(notifyBase):

    HEADERS = {
        "Content-type": "application/x-www-form-urlencoded",
        "Accept": "text/json",
        "User-Agent": "python2-simpleddns/1.0.0 (lolizeppelin@gmail.com)"
    }

    BASEPARAMS = {

    }

    def __init__(self):
        self.conf = CONF[config.NAME]


    def notify(self, ipaddr):

        params = dict(
            format='json', lang='en', record_type='A',
            record_line_id=0,
            domain=CONF.domain, sub_domain=CONF.subdomain,
            value=ipaddr,
            login_token='%d,%s' % (self.conf.id, self.conf.token)
        )
        respon = requests.post(self.conf.api + '/Record.Modify', headers=self.HEADERS,
                               data=urllib.urlencode(params), timeout=self.conf.timeout)
        results = json.loads(respon.text)
        return results


    def infoA(self,):
        params = dict(
            format='json', lang='en',
            domain=CONF.domain, sub_domain=CONF.subdomain,
            login_token='%d,%s' % (self.conf.id, self.conf.token)
        )

        respon = requests.post(self.conf.api + '/Monitor.Listsubvalue',
                               headers=self.HEADERS, data=urllib.urlencode(params),
                               timeout=self.conf.timeout)
        results = json.loads(respon.text)
        return results

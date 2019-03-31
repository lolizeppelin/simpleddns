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

    def __init__(self):
        self.conf = CONF[config.NAME]


    @staticmethod
    def _check_code(result):
        code = int(result.get('status')['code'])
        if code != 1:
            raise ValueError('result fail, code %d, msg %s' % (code, result.get('status')['message']))


    def notify(self, ipaddr):
        """
        https://www.dnspod.cn/docs/records.html#dns
        """
        if ipaddr == self.infoA()['record']['value']:
            return None
        params = dict(
            format='json', lang='en', record_type='A',
            record_line_id="0",
            domain=CONF.domain, sub_domain=CONF.subdomain,
            record_id=self.conf.record_id,
            value=ipaddr,
            login_token='%d,%s' % (self.conf.id, self.conf.token)
        )
        respon = requests.post(self.conf.api + '/Record.Ddns', headers=self.HEADERS,
                               data=urllib.urlencode(params), timeout=self.conf.timeout)
        result = json.loads(respon.text)
        self._check_code(result)
        return result


    def infoA(self):
        params = dict(
            format='json', lang='en',
            domain=CONF.domain, record_id=self.conf.record_id,
            login_token='%d,%s' % (self.conf.id, self.conf.token)
        )

        respon = requests.post(self.conf.api + '/Record.Info',
                               headers=self.HEADERS, data=urllib.urlencode(params),
                               timeout=self.conf.timeout)
        result = json.loads(respon.text)
        self._check_code(result)
        return result


    def infoD(self):
        params = dict(
            format='json', lang='en', record_type='A', record_line_id="0",
            domain=CONF.domain, sub_domain=CONF.subdomain,
            login_token='%d,%s' % (self.conf.id, self.conf.token)
        )

        respon = requests.post(self.conf.api + '/Record.List',
                               headers=self.HEADERS, data=urllib.urlencode(params),
                               timeout=self.conf.timeout)
        result = json.loads(respon.text)
        return result

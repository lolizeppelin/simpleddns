from simpleddns.address import addresBase
from oslocfg import cfg

CONF = cfg.CONF

class addresHelper(addresBase):

    def getaddr(self):
        if CONF.ethernet:
            self._ipaddr = self.check(self._address_of_physical_interface(CONF.ethernet))
        elif CONF.guess:
            self._ipaddr = self.guess_external_ipaddr()
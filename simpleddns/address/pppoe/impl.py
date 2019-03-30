from simpleddns.address import addresBase
from oslocfg import cfg

CONF = cfg.CONF

class addresHelper(addresBase):

    def getaddr(self):
        if CONF.ethernet:

            for addr in self._address_of_physical_interface(CONF.ethernet):
                ethernet = self.check(addr, external=True, raise_error=False)
                if ethernet is not None:
                    self._ipaddr = ethernet
                    return
        elif CONF.guess:
            self._ipaddr = self.guess_external_ipaddr()
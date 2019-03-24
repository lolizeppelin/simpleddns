import os
import socket
import fcntl
import struct
import netaddr
from netaddr import IPNetwork

from oslocfg import cfg

CONF = cfg.CONF

CLASSA = IPNetwork('10.0.0.0/255.0.0.0')
CLASSB = IPNetwork('172.16.0.0/255.240.0.0')
CLASSC = IPNetwork('192.168.0.0/255.255.0.0')
CLASST = IPNetwork('100.64.0.0/255.192.0.0')

INTERNALS = frozenset([CLASSA, CLASSB, CLASSC, CLASST])


def register_guess(name, func):
    addresBase.GUESSPLUGUNS.setdefault(name, func)




class addresBase(object):

    GUESSPLUGUNS = {}

    def __init__(self):

        self._ipaddr = None
        self._lastaddr = None

        self.cfile = os.path.join(CONF.rundir, 'ipaddr')
        if os.path.exists(self.cfile):
            if os.path.getsize(self.cfile) > 1024:
                raise ValueError('ip address state file over size')
            with open(self.cfile, 'r') as f:
                raw = f.read().strip()
                if raw:
                    self._lastaddr = self.check(raw)

    def getaddr(self):
        """get external address!! external!!"""
        raise NotImplementedError

    @property
    def ipaddr(self):
        if self._ipaddr:
            return self._ipaddr
        raise ValueError('External address is None')

    @property
    def last(self):
        return self._lastaddr

    @property
    def modified(self):
        if self._ipaddr is not None:
            return self._ipaddr == self._lastaddr
        return False

    def flush(self):
        if self._ipaddr and self.modified:
            with open(self.cfile, 'w') as f:
                f.write(self._ipaddr)

    def guess_external_ipaddr(self):
        if CONF.guess:
            guess_ip = self.GUESSPLUGUNS[CONF.guess]()
            if guess_ip:
                return self.check(guess_ip)
        return None

    @staticmethod
    def check(address, external=True):
        if not netaddr.valid_ipv4(address, netaddr.core.INET_PTON):
            raise ValueError("%s is not IPv4 or IPv6 address" % address)
        if external:
            for network in INTERNALS:
                if netaddr.IPAddress(address) in network:
                    raise ValueError('Address %s is not external address')
        return address

    @staticmethod
    def _address_of_physical_interface(ifname):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        return socket.inet_ntoa(fcntl.ioctl(
            s.fileno(),
            0x8915,  # SIOCGIFADDR
            struct.pack('256s', ifname[:15])
        )[20:24])

    @staticmethod
    def _guess_external_ipaddr_by_udp():
        """guess external ipaddress by udp"""
        s = None
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(('8.8,8.8', 80))
            return s.getsockname()[0]
        except Exception:
            return None
        finally:
            if s:
                s.close()


register_guess('udp', addresBase._guess_external_ipaddr_by_udp)
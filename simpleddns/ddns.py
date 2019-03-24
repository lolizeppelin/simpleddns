import os
import sys
import contextlib
from oslocfg import cfg

CONF = cfg.CONF

class Ddns(object):

    def __init__(self):
        self.helper = None

    def prepare(self):

        if os.getuid() != 0:
            raise ValueError('Run user error')

        helper = 'simpleddns.address.%s.impl' % CONF.etype
        notifier = 'simpleddns.plugins.%s' % CONF.plugin
        __import__(helper)
        __import__(notifier)

        helper = sys.modules[helper]
        cls = getattr(helper, 'addresHelper')
        self.helper = cls()
        self.helper.getaddr()


    @contextlib.contextmanager
    def logging(self):
        try:
            yield
        except Exception as e:
            import logging
            logging.error(e.message)
            sys.exit(1)


    def notify(self):
        if self.helper.modified:
            notifier = 'simpleddns.plugins.%s.impl' % CONF.plugin
            notifier = sys.modules[notifier]
            cls = getattr(notifier, 'notifyHelper')
            notifier = cls()
            notifier.notify(self.helper.ipaddr)
            self.helper.flush()

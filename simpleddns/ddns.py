import os
import sys
import signal
import contextlib
import threading
from oslocfg import cfg

CONF = cfg.CONF


class SignalHandler(object):
    """Systemd TimeoutStartSec"""

    IGNORE  = frozenset(['SIG_DFL', 'SIG_IGN'])

    def __init__(self):
        self._signals_by_name = dict((name, getattr(signal, name))
                                     for name in dir(signal)
                                     if name.startswith("SIG")
                                     and name not in self.IGNORE)

    def handle_signal(self, handle):
        for signame in ('SIGTERM', 'SIGHUP', 'SIGINT'):
            signo = self._signals_by_name[signame]
            signal.signal(signo, handle)



class Ddns(object):

    def __init__(self):
        self.helper = None

        def kill(signo, frame):
            sys.exit(1)

        SignalHandler().handle_signal(kill)
        timer = threading.Timer(CONF.timeout, lambda : sys.exit(1))
        timer.setDaemon(True)
        timer.start()


    def prepare(self):

        if os.getuid() == 0:
            raise ValueError('Run user error, no root')

        helper = 'simpleddns.address.%s.impl' % CONF.etype
        notifier = 'simpleddns.plugins.%s.impl' % CONF.plugin
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
            if CONF.logging:
                import logging
                logging.error(e.message if e.message else str(e))
            sys.exit(1)

    def notify(self):
        if self.helper.modified:
            notifier = 'simpleddns.plugins.%s.impl' % CONF.plugin
            notifier = sys.modules[notifier]
            cls = getattr(notifier, 'notifyHelper')
            notifier = cls()
            resut = notifier.notify(self.helper.ipaddr)
            self.helper.flush()
            if CONF.loging:
                import logging
                if resut:
                    logging.info("success update ipaddr")
                else:
                    logging.info("succes but do nothing")

from oslocfg import cfg
from simpleddns.config import ddns_opts
import json

CONF = cfg.CONF

CONF.register_cli_opts(ddns_opts)
CONF(project='ddns', default_config_files=['/etc/simpleddns/ddns.conf', ])

def main():
    from simpleddns.plugins.dnspod.impl import notifyHelper
    notifier = notifyHelper()
    print json.dumps(notifier.infoD(), indent=4)
    print '------------------------------------'
    print json.dumps(notifier.infoA(), indent=4)


if __name__ == '__main__':
    main()

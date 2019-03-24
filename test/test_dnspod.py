from oslocfg import cfg
from simpleddns.config import ddns_opts
import json

CONF = cfg.CONF

CONF.register_cli_opts(ddns_opts)
CONF(project='ddns', default_config_files=[r'D:\backup\etc\ddns.conf', ])

def main():
    from simpleddns.plugins.dnspod.impl import notifyHelper
    notifier = notifyHelper()
    data = notifier.infoA()
    print json.dumps(data, indent=4)


if __name__ == '__main__':
    main()

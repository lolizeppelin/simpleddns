from oslocfg import cfg
from simpleddns.config import ddns_opts

CONF = cfg.CONF

CONF.register_cli_opts(ddns_opts)
CONF(project='ddns', default_config_files=['/etc/simpleddns/ddns.conf', ])

def main():
    from simpleddns.address.pppoe.impl import addresHelper
    helper = addresHelper()
    print helper.guess_external_ipaddr()
    print helper.last

if __name__ == '__main__':
    main()

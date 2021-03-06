from oslocfg import cfg

CONF = cfg.CONF

ddns_opts = [
    cfg.StrOpt('domain',
               required=True,
               help='Ddns domain'),
    cfg.StrOpt('subdomain',
               required=True,
               help='Ddns sub domain'),
    cfg.StrOpt('plugin',
               default='dnspod',
               help='ddns notify plugin'),
    cfg.StrOpt('ethernet',
               short='i',
               help='External ethernet interface name'),
    cfg.StrOpt('etype',
               short='e',
               choices=['dhcp', 'pppoe'],
               default='pppoe',
               help='External ipaddres fetch type'),
    cfg.StrOpt('datadir',
               default='/var/lib/simpleddns',
               help='External ipaddres data path, point to the state directory of systemd'),
    cfg.IntOpt('timeout',
               short='t',
               min=10, max=180,
               default=30,
               help='Ddns process Max run time'),
    cfg.StrOpt('guess',
                default='udp',
                help='Guess the external ipaddr by action'),
    cfg.BoolOpt('force',
               default=False,
               help='Force update ddns server'),
    cfg.BoolOpt('logging',
               default=False,
               help='Logging on'),
]


def list_ddns_opts():
    return ddns_opts
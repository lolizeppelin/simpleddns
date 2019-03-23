from oslocfg import cfg
from oslocfg import types

ddns_opts = [
    cfg.IntOpt('timeout',
               short='t',
               required=True,
               min=5,
               default=60,
               max=3600,
               help='Ddns process Max run time'),
    cfg.StrOpt(
        'etype',
        short='e',
        default='pppoe',
        choices=['pppoe', 'dhcp'],
        help='External network type'),
    cfg.IntOpt('timeout',
               short='t',
               required=True,
               min=5,
               default=60,
               max=3600,
               help='Ddns process Max run time'),
]


def list_ddns_opts():
    return ddns_opts
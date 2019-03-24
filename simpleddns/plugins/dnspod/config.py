from oslocfg import cfg

CONF = cfg.CONF

NAME = 'ddns.dnspod'

opts = [
    cfg.StrOpt('api',
               default='https://dnsapi.cn',
               help='Dnspod modify recode api address'),
    cfg.IntOpt('id',
               help='Dnspod api token id'),
    cfg.StrOpt('token',
               help='Dnspod api token'),
    cfg.IntOpt('record_id',
               help='Sub domain record id on dnspod'),
    cfg.IntOpt('timeout',
               max=30, min=1,
               default=5,
               help='Dnspod api request timeout')
]


def register_opts():
    group = cfg.OptGroup(NAME)
    CONF.register_group(group)
    CONF.register_opts(opts, group)
    conf = CONF[NAME]

    if not conf.id:
        raise ValueError('dnspod id can not be found')

    if not conf.token:
        raise ValueError('dnspod tonken can not be found')

    if not conf.record_id:
        raise ValueError('Need record id')

    if conf.timeout >= CONF.timeout:
        raise ValueError('client timeout over process timeout')


def list_opts():
    return opts
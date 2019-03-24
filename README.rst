simpleddns
==========

simple ddns util


DDNS触发程序, systemd定时器调用
默认支持dnspod, 有需要可以通过插件形式
载入其他ddns的api


使用systemctrl edit ddns.timer编辑
::


    [Timer]
    OnUnitActiveSec=5m


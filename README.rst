simpleddns
==========

simple ddns util


DDNS触发程序, systemd定时器调用
默认支持dnspod, 有需要可以通过插件形式
载入其他ddns的api

需要修改间隔请使用如下命令插入内容

systemctl edit ddns.timer
=========================
::


    [Timer]
    OnUnitActiveSec=5m


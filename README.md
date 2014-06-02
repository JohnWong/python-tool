geoip
=====

Convert from ip to geo location. 将ip地址转换为地理地址。<br>

Support ipv4 (纯真网络 ipv4地址库) and ipv6 (ZX IPv6地址库).<br>
Support json and xml format


Published Url
---
<a href="http://pytool.sinaapp.com/">pytool.sinaapp.com</a>

Usage
---
/geo?ip={ip}<br>
如果解析北邮内网地址则添加&pos=1<br>
默认返回xml，需要json则添加&type=json<br>
默认编码gbk，需要utf8编码则添加&encoding=utf-8

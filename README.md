Including Two Tools: Geo IP & Social Follow Button

Geo IP
=====

Convert from ip to geo location. 根据IP地址查询所在的地理位置。<br>

Support ipv4 (纯真网络 ipv4地址库) and ipv6 (ZX IPv6地址库).<br>
Support json and xml format


Published Url
---
<a href="http://pytool.sinaapp.com/">pytool.sinaapp.com</a>

Usage
---
使用方法:/geo?ip={ip}&type={json|xml}&encoding={gbk|utf-8}
如果解析北邮内网地址则添加&pos=1

Social Follow Button
======

生成类似<a href="http://ghbtns.com/">ghbtns</a>的关注按钮。包括根据微博ID生成微博按钮，根据Linkedin公开资料生成Linkedin按钮。

Usage
---
http://pytool.sinaapp.com/wb-btn?user={uid}&count={true|false}&size={small|large}&encoding={utf-8|gbk}
http://pytool.sinaapp.com/in-btn?user={pub_profile}&count={true|false}&size={small|large}&encoding={utf-8|gbk}

demo: <a href="http://pytool.sinaapp.com">http://pytool.sinaapp.com</a>

Including Two Tools: Geo IP & Weibo Follow Button

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

Weibo Follow Button
======

根据微博ID生成一个类似Github的按钮

Usage
---
http://pytool.sinaapp.com/wb-btn?user={uid}&count={true|false}&size={small|large}&encoding={utf-8|gbk}
<iframe class="github-btn" style="overflow: hidden;border: 0;" scrolling="no" src="/wb-btn?user=2180280355&count=true&size=small&encoding=utf-8" width="180" height="20" title="Follow on Weibo"></iframe>

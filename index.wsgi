# -*- coding: cp936 -*-
import sae
import re
import sys
from IpQuery import IpQuery

usage = "使用方法:/gep?ip={ip}\n如果解析北邮内网地址则添加&pos=1"
xml_geo = """<?xml version="1.0" encoding="gbk"?>
<geo>
<ip>{0}</ip>
<loc>{1}</loc>
</geo>
"""
json_geo = """{{"geo":{{"ip":"{0}", "loc":"{1}"}}}}"""

ptn_ip = re.compile(r'^ip=([0-9a-f\:\.]{3,51})$')
ptn_pos = re.compile(r'^pos=([0-1]){0,1}$')
ptn_type = re.compile(r'^type=(json|xml){0,1}$')

ipQuery = IpQuery()

def app(environ, start_response):
    status = '200 OK'
    response_headers = [('Content-type', 'text/html; charset=gbk')]
    start_response(status, response_headers)
    path = environ['PATH_INFO']
    param = environ['QUERY_STRING']
    if path == '/geo' and len(param) > 3:
        params = param.strip(' ').lower().split('&')
        ip = type = pos = None
        for sub in params:
            print(sub)
            if ip == None:
                ma = ptn_ip.match(sub)
                if ma != None:
                    ip = ma.group(1)
            if type == None:
                ma = ptn_type.match(sub)
                if ma != None:
                    type = ma.group(1)
            if pos == None:
                ma = ptn_pos.match(sub)
                if ma != None:
                    pos = ma.group(1)
        type = type if type != None else 'xml'
        pos = 1 if pos != None and pos == '1' else 0
        print(ip, type, pos)
        ret = ipQuery.searchIp(ip, pos)
        fmt = json_geo if type == 'json' else xml_geo
        return fmt.format(ip, ret)
    return usage

application = sae.create_wsgi_app(app)

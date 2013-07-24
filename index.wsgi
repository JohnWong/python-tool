# -*- coding: cp936 -*-
import sae
import re
import sys
from IpQuery import IpQuery

usage = "使用方法:"
ptn_geo = re.compile(r"^ip=([0-9a-fA-F\:\.]{3,51})(&pos(=([0-1]){0,1}){0,1}){0,1}$")
ipQuery = IpQuery()

def app(environ, start_response):
    status = '200 OK'
    response_headers = [('Content-type', 'text/plain')]
    start_response(status, response_headers)
    path = environ['PATH_INFO']
    param = environ['QUERY_STRING']
    if path == '/geo':
        g = ptn_geo.match(param)
        if g != None:
            print(g.groups())
            ip = g.group(1)
            print(g.group(4))
            pos = 1 if g.group(4) == "1" else 0
            print(sys.getdefaultencoding())
            ret = ipQuery.searchIp(ip, pos)
            print(repr(ret))
            return ret
    return usage

application = sae.create_wsgi_app(app)

# -*- coding: cp936 -*-
import sae
import urllib2
import json
import re
import sys
from IpQuery import IpQuery

usage = """<h1>IP转地址</h1>
根据IP地址查询所在的地理位置<br>
使用方法:/geo?ip={ip}&type={json|xml}&encoding={gbk|utf-8}<br>
如果解析北邮内网地址则添加&pos=1<br>
<h1>微博按钮</h1>
根据微博ID生成一个类似Github的按钮<br>
使用方法：/wb-btn?user={uid}&count={true|false}&size={small|large}&encoding={utf-8|gbk}<br>
例如http://pytool.sinaapp.com/wb-btn?user=2180280355&count=true&size=small&encoding=utf-8<br>
<iframe style="overflow: hidden;border: 0;" scrolling="no" src="/wb-btn?user=2180280355&count=true&size=small&encoding=utf-8" width="180" height="20" title="Follow on Weibo"></iframe>
<iframe style="overflow: hidden;border: 0;" scrolling="no" src="/in-btn?user=xiaozhe-huang/4b/204/71b&count=true&size=small&encoding=utf-8" width="220" height="20" title="Connect on Linkedin"></iframe>"""

xml_geo = """<?xml version="1.0" encoding="{encoding}"?>
<geo>
<ip>{0}</ip>
<loc>{1}</loc>
</geo>
"""
json_geo = """{{"geo":{{"ip":"{0}", "loc":"{1}"}}}}"""

ptn_ip = re.compile(r'^ip=([0-9a-f\:\.]{3,51})$')
ptn_pos = re.compile(r'^pos=([0-1]){0,1}$')
ptn_type = re.compile(r'^type=(json|xml){0,1}$')
ptn_encoding = re.compile(r'^encoding=(gbk|utf-8){0,1}$')
ptn_user = re.compile(r'.*user=(.*?)($|&)')
ptn_wbencode = re.compile(r'.*encoding=(gbk|utf-8){0,1}($|&)')

ipQuery = IpQuery()

def app(environ, start_response):
    status = '200 OK'
    path = environ['PATH_INFO']
    param = environ['QUERY_STRING']
    if path == '/geo' and len(param) > 3:
        params = param.strip(' ').lower().split('&')
        ip = type = pos = encoding = None
        for sub in params:
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
            if encoding == None:
                ma = ptn_encoding.match(sub)
                if ma != None:
                    encoding = ma.group(1)

        type = type if type != None else 'xml'
        pos = 1 if pos != None and pos == '1' else 0
        encoding = encoding if encoding != None else 'gbk'
        ret = ipQuery.searchIp(ip, pos)
        fmt = json_geo if type == 'json' else xml_geo
        fmt = fmt.replace('{encoding}', encoding)
        contentType = 'application/json' if type == 'json' else 'text/xml' 
        response_headers = [('Content-type', contentType + '; charset=' + encoding), ('Access-Control-Allow-Origin', '*')]
        start_response(status, response_headers)
        if encoding == 'utf-8':
            return fmt.format(ip, ret).decode('gbk').encode(encoding)
        return fmt.format(ip, ret)
    elif path == "/wb-btn":
        match = ptn_user.findall(param)
        if len(match) > 0:
            uid = match[0][0]

            #fetch sina api
            request = urllib2.Request('https://api.weibo.com/2/users/show.json?source=581960115&uid=' + uid)
            response = urllib2.urlopen(request)
            result = response.read()
            obj = json.loads(result)
            profile_url = obj['profile_url'].encode('utf-8')
            screen_name = obj['screen_name'].encode('utf-8')
            followers_count = obj['followers_count']
            with open('weibo-btn.tp', 'r') as file:
                content = file.read()

            encode_match = ptn_wbencode.findall(param)
            encoding = encode_match[0][0] if len(encode_match) > 0 else 'gbk'
            response_headers = [('Content-type', 'text/html; charset=' + encoding)]
            start_response(status, response_headers)
            content = content.replace('${screen_name}', screen_name).replace('${followers_count}', str(followers_count)).replace('${profile_url}', profile_url)
            if encoding == 'utf-8':
                return content
            return content.decode('utf-8').encode(encoding)
        
    elif path == "/in-btn":
        match = ptn_user.findall(param)
        if len(match) > 0:
            uid = match[0][0]

            #fetch linkedin pub
            profile_url = 'https://www.linkedin.com/pub/' + uid
            request = urllib2.Request(profile_url)
            response = urllib2.urlopen(request)
            result = response.read()

            given_match = re.findall("""<span class="given-name">(.*?)</span>""", result)
            given_name = given_match[0] if len(given_match) > 0 else ""
            family_match = re.findall("""<span class="family-name">(.*?)</span>""", result)
            family_name = family_match[0] if len(family_match) > 0 else ""
            screen_name =  given_name + ' ' + family_name
            conn_match = re.findall("""<strong>(\d*?)</strong> connections""", result)
            followers_count = conn_match[0] if len(conn_match) > 0 else ""
            
            with open('linkedin-btn.tp', 'r') as file:
                content = file.read()

            encode_match = ptn_wbencode.findall(param)
            encoding = encode_match[0][0] if len(encode_match) > 0 else 'gbk'
            response_headers = [('Content-type', 'text/html; charset=' + encoding)]
            start_response(status, response_headers)
            content = content.replace('${screen_name}', screen_name).replace('${followers_count}', str(followers_count)).replace('${profile_url}', profile_url)
            if encoding == 'utf-8':
                return content
            return content.decode('utf-8').encode(encoding)
            

    response_headers = [('Content-type', 'text/html; charset=gbk')]
    start_response(status, response_headers)
    return usage

application = sae.create_wsgi_app(app)

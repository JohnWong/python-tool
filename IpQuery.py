# -*- coding: gbk -*-
import re
from Ipdb import Ipdb
from IpBupt import IpBupt

v4db_path = 'db/qqwry.dat'
v6db_path = 'db/ipv6wry.db'

class IpQuery:
    
    v6ptn = re.compile(r'^[0-9a-f:\.]{3,51}$')
    v4ptn = re.compile(r'.*((25[0-5]|2[0-4]\d|[0-1]?\d\d?)\.){3}(25[0-5]|2[0-4]\d|[0-1]?\d\d?)$')

    def __init__(self):
        self.v6db = Ipdb(v6db_path)
        self.v4db = Ipdb(v4db_path)
        self.ipBupt = IpBupt()
    
    def searchIp(self, ip, pos):
        ret = ''
        try:
            v4, v6 = self.parseIp(ip)
            print('v4: %d v6: %d' % (v4, v6))
            if v6 >= 0:
                ret += self.v6db.searchIp(v6)
            if v4 >= 0:
                if ret != '':
                    ret += ' > '
                bupt = self.ipBupt.searchIp(v4) if pos == 1 else None
                if bupt != None:
                    ret +=  bupt
                else:
                    ret +=  self.v4db.searchIp(v4)
        except Exception as e:
            print(e) 
        if ret == '':
            ret = '格式错误' 
        return ret

    def parseIpv4(self, ip):
        sep = ip.rfind(':')
        if sep >= 0:
            ip = ip[sep+1:]
        if self.v4ptn.match(ip) == None:
            return -1
        v4 = 0
        for sub in ip.split('.'):
             v4 = v4 * 0x100 + int(sub)
        return v4

    def parseIpv6(self, ip):
        if self.v6ptn.match(ip) == None:
            return -1
        count = ip.count(':')
        if count >= 8 or count < 2:
            return -1
        ip = ip.replace('::', '::::::::'[0:8-count+1], 1)
        if ip.count(':') < 6:
            return -1
        v6 = 0
        for sub in ip.split(':')[0:4]:
            if len(sub) > 4:
                return -1
            if len(sub) == 0:
                v6 = v6 * 0x10000
            else:
                v6 = v6 * 0x10000 + int(sub, 16)
        return v6
    
    def parseIp(self, ip):
        ip = ip.strip(' ')
        ip.replace('*', '0')
        v4 = self.parseIpv4(ip)
        v6 = self.parseIpv6(ip)
        v2002 = v6 >> (3 * 16)
        if v2002 == 0x2002:
            v4 = (v6 >> 16) & 0xffffffff
        return v4, v6
    
def main():
    ipQuery = IpQuery()
    #ip = '2001:da8:200:900e:0:5efe:182.117.109.0'
    #ip = '42.156.139.1'
    #ip = '182.117.109.0'
    ip = '114.242.248.*'
    result = ipQuery.searchIp(ip, 1)
    print(result)
    
if __name__=='__main__':
    main()

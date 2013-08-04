# -*- coding: gbk -*-
from Util import Util
from BinarySearch import BinarySearch

class Ipdb(BinarySearch):

    except_raw = 0x19
    
    def __init__(self, db_path):
        f = open(db_path, 'rb')
        db = f.read()
        f.close()
        self.db = db
        header = db[0:4]
        print('header: %s' % header)
        if header != 'IPDB'.encode():
            self.type = 4
            self.initV4Db()
        else:
            self.type = 6
            self.initV6Db()

    def initV4Db(self):
        db = self.db
        self.dbAddr = Util.byte2int(db[0:4], False)
        print('dbaddr: %s' % self.dbAddr)
        endAddr = Util.byte2int(db[4:8], False)
        print('endAddr: %s' % endAddr)
        self.osLen = 3
        print('offset: %s' % self.osLen)
        self.ipLen = 4
        print('iplen: %s' % self.ipLen)
        self.dLen = self.osLen + self.ipLen
        self.size = (endAddr - self.dbAddr) / self.dLen
        print('total: %s' % self.size)
        
    def initV6Db(self):
        db = self.db
        self.osLen = Util.byte2int(db[6])
        print('offset: %s' % self.osLen)
        self.ipLen = Util.byte2int(db[7])
        self.dLen = self.osLen + self.ipLen
        print('iplen: %s' % self.ipLen)
        self.size = Util.byte2int(db[8:0x10], False)
        print('total: %s' % self.size)
        self.dbAddr = Util.byte2int(db[0x10: 0x18], False)
        print('dbaddr: %s' % self.dbAddr)
    
    def getSize(self):
        return self.size

    def getData(self, index):
        self.checkIndex(index)
        addr = self.dbAddr + index * self.dLen
        ip = Util.byte2int(self.db[addr: addr + self.ipLen], False)
        return ip
    
    def checkIndex(self, index):
        if index < 0 or index >= self.getSize():
            raise exception
        
    def getLoc(self, index):
        self.checkIndex(index)
        addr = self.dbAddr + index * self.dLen
        ip = Util.byte2int(self.db[addr: addr + self.ipLen], False)
        lAddr = Util.byte2int(self.db[addr + self.ipLen : addr + self.dLen], False)
        print('ip_addr: %d ip: %d lAddr:%d' % (addr, ip, lAddr))
        if self.type == 4:
            lAddr += 4
        loc = self.readLoc(lAddr, True)
        if self.type == 4:
            loc = loc.decode('cp936').encode('gbk')
        if self.type == 6:
            loc = loc.decode('utf-8').encode('gbk')
        return loc

    def readRawText(self, start):
        bs = ''
        if self.type == 4 and start == self.except_raw:
            return bs
        while ord(self.db[start]) != 0:
            bs += self.db[start]
            start += 1
        return bs

    def readLoc(self, start, isTwoPart = False):
        db = self.db
        jType = Util.byte2int(db[start], False)
        print('start1: %d \t%d %d' % ( start, isTwoPart, jType))
        if jType == 1 or jType == 2:
            start += 1
            offAddr = Util.byte2int(db[start:start+self.osLen], False)
            print("off: %d" % offAddr)
            if offAddr == 0:
                return '未知地址'
            print(jType == 1)
            loc = self.readLoc(offAddr, True if jType == 1 else False)
            nAddr = start + self.osLen
        else :
            loc = self.readRawText(start)
            nAddr = start + len(loc) + 1
        if isTwoPart == True and jType != 1:
            print('read part 2')
            partTwo = self.readLoc(nAddr)
            if loc != '' and partTwo != '':
                loc += ' ' + partTwo
        return loc

    def searchIp(self, val):
        index = self.binarySearch(val)
        if index < 0:
            return '未知地址'
        if index > self.getSize()-2:
            index = self.getSize()-2
        return self.getLoc(index)

def main():
    ipdb = Ipdb('db/qqwry.dat')
    ip = 3061148928L
    #ipdb = Ipdb('db/ipv6wry.db')
    #ip = 0x20010da900000000
    print('ip: %d' % ip)
    print(ipdb.searchIp(ip))

if __name__=='__main__':
    main()

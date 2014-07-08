# -*- coding: gbk -*-
class IpBupt:
    
    _bupt = '北京邮电大学 '
    _type = ['教', '学']
    _num = ['一', '二', '三', '四', '五', '六', '七', '八', '九', '十', '十一', '十二', '十三', '十四', '二十九']
    _wl = '无线网'
    _nb = '新科研楼'
    _buptinno = '创新大本营 学十楼北地下室'
    _mb = '主楼'
    _mgl = '明光楼'
    _yet = '尚未收录'

    def searchIp(self, val):
        a1 = val >> 8 * 3
        if a1 != 10:
            return None
        a2 = (val >> 8 * 2) & 0xff
        loc1 = a2 / 100 - 1
        loc2 = a2 % 100 - 1
        ret = self._yet
        if loc1 == 0 and (loc2 == 7 or loc2 == 8): #新科研楼
            ret = self._bupt + self._nb
        elif loc1 == 0 and loc2 == 4: #主楼
            ret = self._bupt + self._mb
        elif loc1 == 0 and loc2 == 6: #明光楼
            ret = self._bupt + self._mgl
        elif loc1 == 0 and loc2 == 9: #创新大本营
            ret = self._bupt + self._buptinno
        elif loc1 < 0 and loc2 == 7: #无线
            ret = self._bupt + self._wl
        elif loc1 >= 0 and loc1 < len(self._type) and loc2 >= 0 and loc2 < len(self._num):
            ret = self._bupt + self._type[loc1]+self._num[loc2]
        return ret

def main():
    ipBupt = IpBupt()
    ip = (((((10 << 8) + 210) << 8) + 8)<< 8)
    #ip = 174522882
    print(ipBupt.searchIp(ip))

if __name__=='__main__':
    main()

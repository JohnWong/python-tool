# -*- coding: gbk -*-
class IpBupt:
    
    _bupt = '�����ʵ��ѧ '
    _type = ['��', 'ѧ']
    _num = ['һ', '��', '��', '��', '��', '��', '��', '��', '��', 'ʮ', 'ʮһ', 'ʮ��', 'ʮ��', 'ʮ��', '��ʮ��']
    _wl = '������'
    _nb = '�¿���¥'
    _buptinno = '���´�Ӫ ѧʮ¥��������'
    _mb = '��¥'
    _mgl = '����¥'
    _yet = '��δ��¼'

    def searchIp(self, val):
        a1 = val >> 8 * 3
        if a1 != 10:
            return None
        a2 = (val >> 8 * 2) & 0xff
        loc1 = a2 / 100 - 1
        loc2 = a2 % 100 - 1
        ret = self._yet
        if loc1 == 0 and (loc2 == 7 or loc2 == 8): #�¿���¥
            ret = self._bupt + self._nb
        elif loc1 == 0 and loc2 == 4: #��¥
            ret = self._bupt + self._mb
        elif loc1 == 0 and loc2 == 6: #����¥
            ret = self._bupt + self._mgl
        elif loc1 == 0 and loc2 == 9: #���´�Ӫ
            ret = self._bupt + self._buptinno
        elif loc1 < 0 and loc2 == 7: #����
            ret = self._bupt + self._wl
        elif loc1 >= 0 and loc1 < len(self._type) and loc2 >= 0 and loc2 < len(self._num):
            ret = self._bupt + self._type[loc1]+self._num[loc2]
        elif a2 == 28:
            ret = self._bupt + self._type[1] + self._num[9]
        return ret

def main():
    ipBupt = IpBupt()
    ip = (((((10 << 8) + 210) << 8) + 8)<< 8)
    ip = (((((10 << 8) + 28) << 8) + 188)<< 8)
    #ip = 174522882
    print(ipBupt.searchIp(ip))

if __name__=='__main__':
    main()

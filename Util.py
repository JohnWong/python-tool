class Util:
    @staticmethod
    def byte2int(bs, big_endian = True):
        ret = 0
        for i in range(len(bs)) if big_endian else range(len(bs)-1, -1, -1):
            ret = 0x100 * ret + ord(bs[i])
        return ret

    @staticmethod
    def byte2hex(bs):
        ret = ''
        for i in range(len(bs)-1, -1, -2):
            ret += hex(Util.byte2int(bs[i-1:i+1], False))[2:]
            ret += ':'
        return ret + "0:0:0:0"


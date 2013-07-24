class BinarySearch:
    
    def getSize():
        pass
    
    def getDate(index):
        pass
    
    def binarySearch(self, key,lo=0,hi=None):
        if not hi:
            hi = self.getSize() - 1
        while lo<=hi:
            if hi - lo <= 1:
                if self.getData(lo) > key:
                    return -1
                elif self.getData(hi) <= key :
                    return hi
                else:
                    return lo
            mid = (lo+hi)//2
            data = self.getData(mid)
            if data>key:
                hi = mid-1
            elif data<key:
                lo = mid
            else:
                return mid
        return -1

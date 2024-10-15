class Bus:
    def __init__(self):
        self.attachedCache = []
        self.traffic = 0
        
    def attachCache(self, cache):
        self.attachedCache.append(cache)
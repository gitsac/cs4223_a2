import threading

class mainMemory:
    def __init__(self) -> None:
        self.mem = {}
        self.lock = threading.Lock()
        # for i in range(0, 4294967296 + 1, 32):
        #     self.mem[i] = 1
        #     print(i)
        #Initialize all possible blocks based on memory address
        
    def writeBack(self):
        #Acquire lock
        
        #Release lock
        return
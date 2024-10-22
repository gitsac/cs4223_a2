class Block:
    def __init__(self, size, blockID):
        self.size = size
        self.blockId = blockID
        self.valid = True
        self.dirty = 0
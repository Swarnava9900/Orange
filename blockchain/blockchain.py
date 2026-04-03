import time
from .block import Block

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        return Block(0, time.time(), "Genesis Block", "0")
    
    def get_latest_block(self):
        return self.chain[-1]
    
    def add_block(self, data):
        prev_hash = self.get_latest_block().hash
        block = Block(len(self.chain), time.time(), data, prev_hash)
        self.chain.append(block)

    def clear_chain(self):
        self.chain = []
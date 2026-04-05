import time
from .block import Block
from utils.logger import logger

class Blockchain:

    difficulty = 4

    def __init__(self):
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        return Block(0, time.time(), "Genesis Block", "0")
    
    def get_latest_block(self):
        return self.chain[-1]
    
    def proof_of_work(self, block):
        logger.info("Mining block...")
        block.nonce = 0
        computed_hash = block.generate_hash()

        while not computed_hash.startswith("0" * Blockchain.difficulty):
            block.nonce += 1
            computed_hash = block.generate_hash()

        logger.info(f"Block mined:{computed_hash}")
        return computed_hash
    
    def add_block(self, data):
        prev_block = self.get_latest_block()
        new_block = Block(
            index=len(self.chain),
            timestamp=time.time(),
            data=data,
            prev_hash=prev_block.hash
        )
        new_block.hash = self.proof_of_work(new_block)
        self.chain.append(new_block)
        logger.info("Successful! Block added.")

    def clear_chain(self):
        self.chain = []
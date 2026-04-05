import hashlib
import json


class Block:

    def __init__(self, index, timestamp, data, prev_hash, nonce=0):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.prev_hash = prev_hash
        self.nonce = nonce
        self.hash = self.generate_hash()

    def generate_hash(self):

        block_data = {
            "index": self.index,
            "timestamp": self.timestamp,
            "data": self.data,
            "prev_hash": self.prev_hash,
            "nonce": self.nonce
        }

        encoded = json.dumps(block_data, sort_keys=True).encode()
        return hashlib.sha256(encoded).hexdigest()
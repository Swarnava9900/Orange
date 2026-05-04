import time
import json

from .block import Block
from models.block_model import BlockModel
from config.db import db
from utils.logger import logger


class Blockchain:

    difficulty = 5

    def __init__(self):
        self.chain = []
        self.pending_transactions = []

        try:
            db_blocks = BlockModel.query.order_by(BlockModel.index).all()

            print(f"DB Blocks Found: {len(db_blocks)}")  # 🧪 debug

            # ✅ If DB has blocks → load them
            if db_blocks:
                for b in db_blocks:
                    block = Block(
                        b.index,
                        b.timestamp,
                        json.loads(b.data),
                        b.prev_hash,
                        b.nonce
                    )
                    block.hash = b.hash
                    self.chain.append(block)

                logger.info("Blockchain loaded from database")

            # ❌ If empty → create genesis
            else:
                logger.warning("No blocks found in DB. Creating genesis block.")

                genesis = self.create_genesis_block()
                self.chain.append(genesis)

                self._save_block_to_db(genesis)

        except Exception as e:
            logger.error(f"Error loading blockchain: {str(e)}")

    # 🔹 Internal helper for DB save
    def _save_block_to_db(self, block):
        try:
            block_model = BlockModel(
                index=block.index,
                timestamp=block.timestamp,
                data=json.dumps(block.data),
                prev_hash=block.prev_hash,
                nonce=block.nonce,
                hash=block.hash
            )

            db.session.add(block_model)
            db.session.commit()

        except Exception as e:
            db.session.rollback()
            logger.error(f"DB write failed: {str(e)}")

    # 🔹 Create genesis block
    def create_genesis_block(self):
        genesis = Block(0, time.time(), "Genesis Block", "0")
        genesis.hash = genesis.generate_hash()
        return genesis

    # 🔹 Proof of Work
    def proof_of_work(self, block):
        logger.info("Mining block...")

        block.nonce = 0
        computed_hash = block.generate_hash()

        while not computed_hash.startswith("0" * Blockchain.difficulty):
            block.nonce += 1
            computed_hash = block.generate_hash()

        block.hash = computed_hash
        logger.info(f"Block mined: {computed_hash}")

        return computed_hash

    # 🔹 Validate chain
    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            prev_block = self.chain[i - 1]

            if current_block.hash != current_block.generate_hash():
                logger.error(f"Invalid hash at block {i}")
                return False

            if current_block.prev_hash != prev_block.hash:
                logger.error(f"Invalid previous hash at block {i}")
                return False

            if not current_block.hash.startswith("0" * Blockchain.difficulty):
                logger.error(f"Invalid proof of work at block {i}")
                return False

        return True

    # 🔹 Get latest block
    def get_latest_block(self):
        return self.chain[-1]

    # 🔹 Clear entire chain (DB + memory)
    def clear_chain(self):
        try:
            BlockModel.query.delete()
            db.session.commit()

            genesis = self.create_genesis_block()
            self.chain = [genesis]

            self._save_block_to_db(genesis)

            logger.warning("Blockchain reset successfully")

        except Exception as e:
            db.session.rollback()
            logger.error(f"Failed to clear blockchain: {str(e)}")

    # 🔹 Add transaction
    def add_transaction(self, transaction):
        self.pending_transactions.append(transaction)
        logger.info("Transaction added to pool")

    # 🔹 Mine transactions
    def mine_pending_transactions(self):
        if not self.is_chain_valid():
            logger.error("Cannot mine: Blockchain is invalid")
            return False

        if not self.pending_transactions:
            logger.warning("No transactions to mine")
            return False

        prev_block = self.get_latest_block()

        new_block = Block(
            index=len(self.chain),
            timestamp=time.time(),
            data=self.pending_transactions.copy(),
            prev_hash=prev_block.hash
        )

        # ⛏️ Mine block
        self.proof_of_work(new_block)

        # 🧠 Add to memory
        self.chain.append(new_block)

        # 💾 Save to DB safely
        self._save_block_to_db(new_block)

        logger.info(f"Block mined with {len(new_block.data)} transactions")

        self.pending_transactions = []

        return True
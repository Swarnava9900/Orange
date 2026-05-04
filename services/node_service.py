import requests
from core.block import Block
from core.blockchain import Blockchain


def register_node(app, address):
    if not address.startswith("http"):
        address = "http://" + address
    app.nodes.add(address)

def get_nodes(app):
    return list(app.nodes)

def check_nodes(app):
    active_nodes = []

    for node in app.nodes:
        try:
            response = requests.get(f"{node}/chain", timeout=3)
            if response.status_code == 200:
                active_nodes.append(node)
        except requests.exceptions.RequestException:
            pass

    return active_nodes

def resolve_conflicts(app):
    blockchain = app.blockchain

    longest_chain = None
    max_length = len(blockchain.chain)

    for node in app.nodes:
        try:
            response = requests.get(f"{node}/chain", timeout=3)

            if response.status_code == 200:
                data = response.json()
                length = data.get("length")
                chain = data.get("chain")

                if not length or not chain:
                    continue

                if length > max_length:
                    if is_valid_external_chain(chain):
                        max_length = length
                        longest_chain = chain

        except requests.exceptions.RequestException:
            continue

    if longest_chain:
        blockchain.chain = reconstruct_chain(longest_chain)
        blockchain.pending_transactions = []
        return True

    return False

def is_valid_external_chain(chain_data):

    if len(chain_data) == 0:
        return False

    if chain_data[0].get("prev_hash") != "0":
        return False

    required_keys = ["index", "timestamp", "data", "prev_hash", "nonce", "hash"]

    for i in range(1, len(chain_data)):
        current = chain_data[i]
        prev = chain_data[i - 1]

        for key in required_keys:
            if key not in current:
                return False

        block_copy = Block(
            current["index"],
            current["timestamp"],
            current["data"],
            current["prev_hash"],
            current["nonce"]
        )

        if block_copy.generate_hash() != current["hash"]:
            return False

        if current["prev_hash"] != prev["hash"]:
            return False

        if not current["hash"].startswith("0" * Blockchain.difficulty):
            return False

    return True

def reconstruct_chain(chain_data):

    new_chain = []

    for block in chain_data:
        b = Block(
            block["index"],
            block["timestamp"],
            block["data"],
            block["prev_hash"],
            block["nonce"]
        )
        b.hash = block["hash"]
        new_chain.append(b)

    return new_chain
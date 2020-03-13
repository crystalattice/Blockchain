import hashlib
import json
import pickle

from time import time
from urllib.parse import urlparse
from Modbus.hashing_server import ModbusTransaction


class Blockchain:
    def __init__(self):
        self.chain = []
        self.current_transactions = []
        self.last_proof = None
        self.proof = None
        self.previous_hash = None
        self.block = None
        self.sender = None
        self.recipient = None
        self.modbus_cmd = None

        self.genesis_block = self.new_block(previous_hash=1, proof=100)  # Create the genesis block
        # self.nodes = set()  # List of nodes in blockchain n/w; ensures specific node only appears once

    @property
    def last_block(self):
        """Return last block in chain"""
        return self.chain[-1]

    @last_block.setter
    def last_block(self, block):
        """Add block to end of chain"""
        self.chain.append(block)

    @property
    def full_chain(self):
        """Display the entire blockchain."""
        return {"chain": self.chain, "length": len(self.chain)}

    @staticmethod
    def pickle_cmd(cmd):
        """Serialize modbus command."""
        with open("cmd.pickle", "wb") as modbus_cmd:
            pickle.dump(cmd, modbus_cmd)

    @staticmethod
    def pickle_block(block):
        """Serialize hashed block"""
        with open("block.pickle", "wb") as modbus_block:
            pickle.dump(block, modbus_block)

    @staticmethod
    def create_hash(block):
        """Create a hash digest of a block"""
        block_string = json.dumps(block, sort_keys=True).encode()

        return hashlib.sha256(block_string).hexdigest()

    @staticmethod
    def valid_proof(last_proof, proof):
        """Validates proof of work"""
        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()

        return guess_hash[:4] == "0000"

    # def register_node(self, address):
    #     """Add a new node to the list of n/w nodes"""
    #     Get node URL address
    #     parsed_url = urlparse(address)
    #     self.nodes.add((parsed_url.netloc))
    #
    #     self.nodes.add(address)

    def new_block(self, proof, previous_hash=None):
        """Creates a new block and adds it to the chain"""
        block = {
            "index": len(self.chain) + 1,
            "timestamp": time(),
            "transactions": self.current_transactions,
            "proof": proof,
            "previous_hash": previous_hash or self.create_hash(self.chain[-1])
        }

        self.current_transactions = []  # Reset the current transactions list
        self.chain.append(block)  # Add new block to chain

        return block

    def proof_of_work(self, last_proof):
        """Proof of work algorithm.

        Find a number (p`) such that hash(pp`) contains 4 ending zeros, where p is the previous p`
        'p' is the previous proof; 'p`' is the new proof
        """
        proof = 0
        while not self.valid_proof(last_proof, proof):
            proof += 1

        return proof

    def mine(self, sender, recipient, cmd_and_hash):
        """Mines a new block"""
        # Get next proof
        self.last_proof = self.last_block["proof"]
        self.proof = self.proof_of_work(self.last_proof)

        # Mine a new coin
        self.add_transaction(sender, recipient, cmd_and_hash)

        # Add new block to chain
        self.previous_hash = self.create_hash(self.last_block)
        self.block = self.new_block(self.proof, self.previous_hash)

        response = {
            "message": "New block forged",
            "index": self.block["index"],
            "transactions": self.block["transactions"],
            "proof": self.block["proof"],
            "previous_hash": self.block["previous_hash"]
        }

        return response

    def new_transaction(self, sender, recipient, cmd_and_hash):
        """Adds a new transaction to the list of transactions.

        The returned index is the index of the next transaction to be mined.
        """
        self.current_transactions.append({"sender": sender, "recipient": recipient, "cmd_tuple": cmd_and_hash})

        return self.last_block["index"] + 1  # Block index of this new transaction

    def add_transaction(self, sender, recipient, cmd):
        """Add a new transaction to chain."""
        # Check for valid data
        if not sender:
            raise ValueError("Missing 'sender'")
        elif not recipient:
            raise ValueError("Missing 'recipient'")
        elif not cmd:
            raise ValueError("Missing 'modbus_cmd'")
        else:
            self.sender = sender
            self.recipient = recipient
            self.modbus_cmd = cmd

        # Make new transaction
        index = self.new_transaction(self.sender, self.recipient, self.modbus_cmd)
        return "Transaction will be added to block {}".format(index)

    # def valid_chain(self, chain):
    #     """Determine if a chain is valid"""
    #     last_block = chain[0]
    #     current_index = 1
    #
    #     while current_index < len(chain):
    #         block = chain[current_index]
    #         print("Last block = {}".format(last_block))
    #         print("Current block = {}".format(block))
    #         print("\n---------\n")
    #
    #         # Check that the current block's hash is correct
    #         if block["previous_hash"] != self.hash(last_block):
    #             return False
    #
    #         # Check proof of work is correct
    #         if not self.valid_proof(last_block["proof"], block["proof"]):
    #             return False
    #
    #         last_block = block
    #         current_index += 1
    #
    #     return True

    # def resolve_conflicts(self):
    #     """Consensus algorithm
    #
    #     Resolves conflicts by replacing current chain with longest one on n/w. Assumes longest chain is the only
    #     valid chain.
    #     """
    #     neighbors = self.nodes
    #     new_chain = None
    #
    #     # Look for chains longer than current
    #     max_length = len(self.chain)
    #
    #     # Verify chains from all n/w nodes
    #     for node in neighbors:
    #         node_length = node.full_chain()["length"]
    #         node_chain = node.full_chain()["chain"]
    #
    #         # Check if node chain longer than current chain
    #         if node_length > max_length and self.valid_chain(node_chain):
    #             max_length = node_length
    #             new_chain = node_chain
    #
    #     # Replace current chain if node chain is longer
    #     if new_chain:
    #         self.chain = new_chain
    #         return True
    #
    #     return False

    # def register_nodes(self, nodes):
    #     if not nodes:
    #         raise ValueError("Please supply a valid list of nodes")
    #     else:
    #         for node in nodes:
    #             self.register_node(node)
    #
    #     return "New nodes have been added\nNodes: {}".format(list(self.nodes))

    # def consensus(self):
    #     replaced = self.resolve_conflicts()
    #
    #     if replaced:
    #         return "Our chain was replaced with {}".format(self.chain)
    #     else:
    #         return "Our chain is accurate. Chain is {}".format(self.chain)


if __name__ == "__main__":
    blockchain = Blockchain()
    transaction = ModbusTransaction()
    transaction.establish_conn()
    node_identifier = "127.0.0.1"
    print(blockchain.genesis_block)
    print(blockchain.mine(sender=node_identifier, recipient="someone_else", cmd_and_hash=transaction.cmd_and_hash()))
    # print(blockchain.mine(sender=node_identifier, recipient="someone_else", cmd_and_hash=transaction.cmd_and_hash()))
    # print(json.dumps(blockchain.full_chain(), sort_keys=True, indent=4))  # Pretty print blockchain
    print(blockchain.full_chain)
    transaction.close_conn()

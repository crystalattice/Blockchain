import hashlib
import json
import time
import uuid


class Blockchain:
    def __init__(self):
        self.chain = []
        self.current_transactions = []

        self.new_block(previous_hash=1, proof=100)  # Create the genesis block

    def new_block(self, proof, previous_hash=None):
        """Creates a new block and adds it to the chain

        :param proof: Proof of work
        :param previous_hash: Hash of previous block (optional)

        :return: New block
        """
        block = {"index": len(self.chain) + 1, "timestamp": time.time(), "transactions": self.current_transactions,
                 "proof": proof, "previous_hash": previous_hash or self.hash(self.chain[-1])}

        self.current_transactions = []  # Reset the current transactions list
        self.chain.append(block)  # Add new block to chain

        return block

    def new_transaction(self, sender, recipient, amount):
        """Adds a new transaction to the list of transactions.

        The returned index is the index of the next transaction to be mined.

        :param sender: Address of sender
        :param recipient: Address of recipient
        :param amount: Transaction amount

        :return: The block index that holds this transaction
        """
        self.current_transactions.append({"sender": sender, "recipient": recipient, "amount": amount})

        return self.last_block["index"] + 1  # Block index of this new transaction

    @staticmethod
    def hash(block):
        """Create a hash digest of a block

        :param block: Block

        :return: Hash string
        """
        block_string = json.dumps(block, sort_keys=True).encode()

        return hashlib.sha256(block_string).hexdigest()

    @property
    def last_block(self):
        """Return last block in chain"""
        return self.chain[-1]

    def proof_of_work(self, last_proof):
        """Proof of work algorithm.

        Find a number (p`) such that hash(pp`) contains 4 ending zeros, where p is the previous p`
        'p' is the previous proof; 'p`' is the new proof

        :param last_proof: Integer

        :return: Integer
        """
        proof = 0
        while self.valid_proof(last_proof, proof) == False:
            proof += 1

        return proof

    @staticmethod
    def valid_proof(last_proof, proof):
        """Validates proof of work

        :param last_proof: Previous proof
        :param proof: Current proof

        :return: True if correct, False if not
        """
        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()

        return guess_hash[:4] == "0000"
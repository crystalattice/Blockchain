import time
import hashlib
import pickle


class Block(object):
    def __init__(self, index, new_proof, previous_hash, transactions, timestamp=time.time()):
        self.index = index
        self.proof = new_proof
        self.previous_hash = previous_hash
        self.transactions = transactions
        self.timestamp = timestamp

    @property
    def get_block_hash(self):
        block_string = f"{self.index}{self.proof}{self.previous_hash}{self.transactions}{self.timestamp}"
        return hashlib.sha256(block_string.encode()).hexdigest()

    def __repr__(self):
        return f"Block index:{self.index} - List of transactions:{self.transactions} - Block timestamp:{self.timestamp}"
        # return "{} - {} - {} - {} - {}".format(self.index, self.proof, self.previous_hash, self.transactions,
        #                                        self.timestamp)


class BlockChain(object):
    def __init__(self):
        self.chain = []
        self.current_node_transactions = []
        self.nodes = set()
        self.create_genesis_block()

    @property
    def get_serialized_chain(self):
        return [vars(each_block) for each_block in self.chain]

    @staticmethod
    def pickle_cmd(cmd):
        """Serialize modbus command for JSON object."""
        modbus_pickle = cmd.pickle()

        return modbus_pickle

    def create_genesis_block(self):
        self.create_new_block(block_proof=0, previous_hash=0)

    def create_new_block(self, block_proof, previous_hash):
        new_block = Block(
            index=len(self.chain),
            new_proof=block_proof,
            previous_hash=previous_hash,
            transactions=self.current_node_transactions
        )
        self.current_node_transactions = []  # Reset the transaction list

        self.chain.append(new_block)
        return new_block

    @staticmethod
    def is_valid_block(block, previous_block):
        if previous_block.index + 1 != block.index:
            return False
        elif previous_block.get_block_hash != block.previous_hash:
            return False
        elif not BlockChain.is_valid_proof(block.current_proof, previous_block.current_proof):
            return False
        elif block.timestamp <= previous_block.timestamp:
            return False
        return True

    def create_new_transaction(self, sender, recipient, amount):
        self.current_node_transactions.append(dict(sender=sender, recipient=recipient, amount=amount))
        return True

    @staticmethod
    def is_valid_transaction():
        # Not Implemented
        pass

    @staticmethod
    def create_proof_of_work(previous_proof):
        """
        Generate "Proof Of Work"

        A very simple `Proof of Work` Algorithm -
            - Find a number such that, sum of the number and previous POW number is divisible by 7
        """
        new_proof = previous_proof + 1
        while not BlockChain.is_valid_proof(new_proof, previous_proof):
            new_proof += 1

        return new_proof

    @staticmethod
    def is_valid_proof(new_proof, previous_proof):
        return (new_proof + previous_proof) % 7 == 0

    @property
    def get_last_block(self):
        return self.chain[-1]

    def is_valid_chain(self):
        """
        Check if given blockchain is valid
        """
        previous_block = self.chain[0]
        current_index = 1

        while current_index < len(self.chain):
            current_block = self.chain[current_index]
            if not self.is_valid_block(current_block, previous_block):
                return False
            previous_block = current_block
            current_index += 1
        return True

    def mine_block(self, miner_address):
        # Sender "0" means that this node has mined a new block
        # For mining the Block(or finding the new_proof), we must be awarded with some amount(in our case this is 1)
        self.create_new_transaction(sender="0", recipient=miner_address, amount=1)

        previous_block = self.get_last_block

        previous_proof = previous_block.current_proof
        new_proof = self.create_proof_of_work(previous_proof)

        previous_hash = previous_block.get_block_hash
        new_block = self.create_new_block(new_proof, previous_hash)

        return vars(new_block)  # Return a native Dict type object

    def create_node(self, address):
        self.nodes.add(address)
        return True

    @staticmethod
    def get_block_object_from_block_data(block_data):
        return Block(
            block_data['index'],
            block_data['proof'],
            block_data['previous_hash'],
            block_data['transactions'],
            timestamp=block_data['timestamp']
        )


if __name__ == "__main__":
    block_chain = BlockChain()

    print(">>>>> Before Mining...")
    print(block_chain.chain)

    last_block = block_chain.get_last_block
    last_proof = last_block.current_proof
    proof = block_chain.create_proof_of_work(last_proof)

    # Sender "0" means that this node has mined a new block
    # For mining the Block(or finding the proof), we must be awarded with some amount(in our case this is 1)
    block_chain.create_new_transaction(
        sender="0",
        recipient="address_x",
        amount=1,
    )
    last_hash = last_block.get_block_hash
    block = block_chain.create_new_block(proof, last_hash)

    print(">>>>> After Mining...")
    for blocks in block_chain.chain:
        print(blocks)

import Crypto
import Crypto.Random
from Crypto.Hash import SHA
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
import hashlib
import random
import string
import json
import binascii
import numpy as np
import pandas as pd
# import pylab as pl
import logging
import datetime
import collections

transactions = []
last_block_hash = ""
TPCoins = []
last_transaction_index = 0


class Client:
    def __init__(self):
        random_seed = Crypto.Random.new().read
        self._private_key = RSA.generate(1024, random_seed)
        self._public_key = self._private_key.publickey()
        self._signer = PKCS1_v1_5.new(self._private_key)

    @property
    def identity(self):
        return binascii.hexlify(self._public_key.exportKey(format="DER")).decode("ascii")


class Transaction:
    def __init__(self, sender, recipient, value):
        self.sender = sender
        self.recipient = recipient
        self.value = value
        self.time = datetime.datetime.now()

    def transaction_to_dict(self):
        if self.sender == "Genesis":
            identity = "Genesis"
        else:
            identity = self.sender.identity

        return {"sender": identity, "recipient": self.recipient, "value": self.value, "time": self.time}

    def sign_transaction(self):
        private_key = self.sender._private_key
        signer = PKCS1_v1_5.new(private_key)
        signing_hash = SHA.new(str(self.transaction_to_dict()).encode("utf8"))

        return binascii.hexlify(signer.sign(signing_hash)).decode("ascii")


class Block:
    def __init__(self):
        self.verified_transactions = []
        self.previous_hash = ""
        self.current_hash = ""

    def dump_blockchain(self):
        print(f"Number of blocks in the chain {len(self)}")
        for i in range(len(TPCoins)):
            temp_block = TPCoins[i]
            print(f"Block #{i}")
            for transaction in temp_block.verified_transactions:
                display_transaction(transaction)
                print("------------------------")
            print("=============================")


# def add_block():
#     global last_transaction_index
#     global last_block_hash
#     block = Block()
#     for i in range(3):  # Get top 3 transactions from queue
#         temp_transaction = transactions[last_transaction_index]
#         # validate transaction
#         # if valid
#         block.verified_transactions.append(temp_transaction)
#         last_transaction_index += 1
#
#     block.previous_hash = last_block_hash
#     block.current_hash = mine(block, 2)
#     digest = hash(block)
#     TPCoins.append(block)
#     last_block_hash = digest
#
#     return


def display_transaction(trans):
    output = trans.transaction_to_dict()
    print(f"sender: {output['sender']}")
    print('-----')
    print(f"recipient: {output['recipient']}")
    print('-----')
    print(f"value: {str(output['value'])}")
    print('-----')
    print(f"time: {str(output['time'])}")
    print('-----')


def create_genesis_block(recipient, value):
    global last_block_hash

    t0 = Transaction("Genesis", recipient, value)  # Initial transaction

    # Generate genesis block
    block0 = Block()
    block0.previous_hash = None
    last_block_hash = None

    block0.verified_transactions.append(t0)  # Add initial transaction to list
    digest = hash(block0)  # Hash genesis block
    last_block_hash = digest  # Track previous (genesis) block

    return block0, digest


def sha256(msg):
    return hashlib.sha256(msg.encode("ascii")).hexdigest()


def mine(msg, difficulty=1):
    try:
        if difficulty < 1:
            raise ValueError
        prefix = "1" * difficulty
        for i in range(10000000):
            digest = sha256(str(hash(msg)) + str(i))
            if digest.startswith(prefix):
                print(f"After {i} iterations, found digest {digest}")
                return digest
    except ValueError:
        print("Mining difficulty must be > 1")


# block = Block()
# for i in range(3):  # Get top 3 transactions from queue
#     temp_transaction = transactions[last_transaction_index]
#     # validate transaction
#     # if valid
#     block.verified_transactions.append(temp_transaction)
#     last_transaction_index += 1
#
# block.previous_hash = last_block_hash
# block.current_hash = mine(block, 2)
# digest = hash(block)
# TPCoins.append(block)
# last_block_hash = digest

if __name__ == "__main__":
    # Create genesis block
    create_genesis_block("Miner 1", 500.0)

    block = Block()
    for i in range(0):  # Get top 3 transactions from queue
        temp_transaction = transactions[last_transaction_index]
        # validate transaction
        # if valid
        block.verified_transactions.append(temp_transaction)
        last_transaction_index += 1

    block.previous_hash = last_block_hash
    block.current_hash = mine(block, 2)
    digest = hash(block)
    TPCoins.append(block)
    last_block_hash = digest

    # # Miner 1
    # add_block()
    #
    # # Miner 2
    # add_block()
    #
    # # Miner 3
    # add_block()
import json
import hashlib


def hash_function(block):
    """Hashes our transaction."""
    if type(block) != str:
        block = json.dumps(block, sort_keys=True).encode()

    return hashlib.sha256(block).hexdigest()


def update_state(transaction, state):
    """Updates record of owners.

    Makes a copy of the current state then, for each transaction owner, check if the owner is also present in the
    state record. If so, add the owner's transaction value to the state value. Otherwise, add the owner and value to the
    state record.

    :param transaction: Dictionary of owner:amount
    :param state: Dictionary of transactions

    :return: Updated record of owners and amounts
    """
    state = state.copy()

    for key in transaction:
        if key in state.keys():
            state[key] += transaction[key]
        else:
            state[key] = transaction[key]

    return state


def valid_transaction(transaction, state):
    """A valid transaction must sum to 0.

    The sum of all the values in the transaction dict must equal zero. If not, the transaction is invalid.

    Check if the transaction owner is also present in the state record. If so, the owner's state value is the current
    account balance. If the owner doesn't exist, the account balance is zero.

    If the account balance and owner's transaction value are less than zero, the transaction is invalid.
    """
    if sum(transaction.values()) != 0:
        return False

    for key in transaction.keys():
        if key in state.keys():
            account_balance = state[key]
        else:
            account_balance = 0

        if account_balance + transaction[key] < 0:
            return False

    return True


def make_block(transactions, chain):
    """Make a block to go into the chain. References last transaction in the current chain for new values. This prevents
    fraudulent blocks from being inserted into the chain, as they don't know the transaction history.

    The parent hash is the hash digest from the last transaction in the current chain.
    The block number is the block number from the last transaction in the current chain, incremented by one.

    :param transactions: Dictionary of owner:amount
    :param chain: Current blockchain

    :return: Dictionary of current block's hash digest and the actual contents of the current block.
    """
    parent_hash = chain[-1]['hash']
    block_number = chain[-1]['contents']['block_number'] + 1

    block_contents = {
        'block_number': block_number,
        'parent_hash': parent_hash,
        'transaction_count': block_number + 1,
        'transaction': transactions
    }

    return {'hash': hash_function(block_contents), 'contents': block_contents}


def check_block_hash(block):
    """Check the hash of a block.

    If the embedded hash value of the block doesn't equal the computed digest of the block's contents, the block is
    invalid.
    """
    expected_hash = hash_function(block['contents'])

    if block['hash'] != expected_hash:
        raise Exception

    return  # Empty return not necessary


def check_block_validity(block, parent, state):
    """Check the block has valid parameters.

    Parent number is the block number from the previous block in current chain.
    Parent hash is the hash digest from the previous block.
    Block number is the previous block's index value.

    For each transaction in the current block, validate the transaction with the record state. If the transaction is
    valid, update the record state with the current owner:amount elements. If not valid, raise an exception.

    Next, validate the current block's hash digest. Then, confirm that the current block index number is equal to the
    parent's index + 1. Finally, check whether the parent hash digest contained within the block content is equal to
    the digest stored in the parent block itself.
    """
    parent_number = parent['contents']['block_number']
    parent_hash = parent['hash']
    block_number = block['contents']['block_number']

    for transaction in block['contents']['transaction']:
        if valid_transaction(transaction, state):
            state = update_state(transaction, state)
        else:
            raise Exception

    check_block_hash(block)  # Check hash integrity

    if block_number != parent_number + 1:
        raise Exception

    if block['contents']['parent_hash'] != parent_hash:
        raise Exception

    return state


def check_chain(chain):
    """Check the chain is valid.

    Confirms that the blockchain argument is a Python list. If not, the chain is invalid.

    For each transaction in the chain, update the record state with that transaction information. Next, validate the
    chain's initial block's hash, then set the parent block to the initial block.

    For the remaining blocks in the chain, validate each block's parameters and put the result into the state
    dictionary, then reset the parent block to the now-validated block.
    """
    if type(chain) is str:
        try:
            chain = json.loads(chain)
            assert (type(chain) == list)
        except ValueError:
            # String passed in was not valid JSON
            return False
    elif type(chain) != list:
        return False

    state = {}

    for transaction in chain[0]['contents']['transaction']:
        state = update_state(transaction, state)

    check_block_hash(chain[0])
    parent = chain[0]

    for block in chain[1:]:
        state = check_block_validity(block, parent, state)
        parent = block

    return state


def add_transaction_to_chain(transaction, state, chain):
    """Places the current transaction block into the chain.

    If the transaction is validated, the record state is updated, otherwise an exception is generated.

    A new block is created and appended to the current chain. For each transaction listed in the current chain, a
    validation check is made.
    """
    if valid_transaction(transaction, state):
        state = update_state(transaction, state)
    else:
        raise Exception('Invalid transaction.')

    my_block = make_block(state, chain)
    chain.append(my_block)

    for transaction in chain:
        check_chain(transaction)

    return state, chain


if __name__ == "__main__":
    genesis_block = {
        'hash': hash_function({
            'block_number': 0,
            'parent_hash': None,
            'transaction_count': 1,
            'transaction': [{'Tom': 10}]
        }),
        'contents': {
            'block_number': 0,
            'parent_hash': None,
            'transaction_count': 1,
            'transaction': [{'Tom': 10}]
        },
    }

    block_chain = [genesis_block]
    chain_state = {'Tom': 10}

    chain_state, block_chain = add_transaction_to_chain(transaction={'Tom': -1, 'Medium': 1}, state=chain_state,
                                                        chain=block_chain)
    print(chain_state)
    print(json.dumps(block_chain, sort_keys=True, indent=4))  # Pretty print blockchain

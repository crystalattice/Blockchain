import random

random.seed(0)


def make_transaction(max_value=3):
    """Creates randomized, valid transactions between 1 and max_value

    Ensures conservation of token transactions, but doesn't check for overdraft
    """
    sign = random.choice((-1, 1))  # Randomly choose 1 or -1
    amount = random.randint(1, max_value)  # Select a random transaction amount
    alice_pays = sign * amount
    bob_pays = -1 * alice_pays

    return {"Alice": alice_pays, "Bob": bob_pays}

def update_state(transaction, state):
    """Updates the state record of owner.

    Does not validate transaction, i.e. it doesn't verify whether the transaction is allowable.
    """
    state = state.copy()  # Creates a copy of the state record

    for key in transaction:
        if key in state.keys():
            state[key] += transaction[key]  # add the transaction key to the state record keys
        else:
            state[key] = transaction[key]  # otherwise, the state record key equals the transaction key

    return state

def valid_transaction(transaction, state):
    """Ensure transaction sum = 0

    Similar to double-entry bookkeeping, additions from one side must equal subtractions from the other.
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
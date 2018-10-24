import hashlib, json, sys


def hash_helper(msg=""):
    """Helper function that wraps the hashing algorithm.

    Checks to see if argument is a string. If not, converts the argument to a JSON string via JSON encoding.
    Keys must be sorted to ensure repeatability.

    Also checks Python version used and returns the appropriate hash digest.
    """
    if type(msg) != str:
        msg = json.dumps(msg, sort_keys=True)  # Serialize msg to JSON formatted str and sort keys

    if sys.version_info.major == 2:  # If using Python 2.x
        return unicode(hashlib.sha256(msg).hexdigest(), 'utf-8')
    else:
        return hashlib.sha256(str(msg).encode('utf-8')).hexdigest()

if __name__ == "__main__":
    print(hash_helper("I will not eat spam"))
    print(hash_helper([1, 2, 3]))

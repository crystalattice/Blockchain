"""Determines how much time is required to get the desired ending values in a hash digest.

Commonly used in blockchain proof of work.
"""

from hashlib import sha256
x = 5
y = 0  # We don't know what y should be yet...
while sha256(f'{x*y}'.encode()).hexdigest()[:7] != "0000000":
    y += 1
print(f'The solution is y = {y}')

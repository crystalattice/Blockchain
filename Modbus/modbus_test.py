import hashlib
import json
import pickle
from pymodbus.client.sync import ModbusTcpClient

client = ModbusTcpClient('127.0.0.1', 5020)
data = client.write_coil(1, True)
hash_val = hashlib.sha256()
with open("client.pickle", "wb") as cmd:
    pickle.dump(data, cmd)
cmd_in = open("client.pickle", "rb")
while True:
    chunk = cmd_in.read(1024)
    if chunk:
        hash_val.update(chunk)
    else:
        hex_hash = hash_val.hexdigest()
        break
print(hex_hash)
result = client.read_coils(1, 1)
print(result.bits[0])
client.close()

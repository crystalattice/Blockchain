import hashlib
import pickle
from pymodbus.client.sync import ModbusTcpClient


class ModbusTransaction:
    def __init__(self, host="localhost", port=5020):
        self.host = host
        self.port = port
        self.client = None
        self.data = None
        self.hash_val = hashlib.sha256()

    def establish_conn(self):
        self.client = ModbusTcpClient(self.host, self.port)

    def write_single_coil(self, address=1, value=False):
        return self.client.write_coil(address, value)

    def read_single_coil(self, address=1, count=1):
        return self.client.read_coils(address, count)

    def serialize_cmd(self, data):
        with open("client.pickle", "wb") as cmd:
            pickle.dump(data, cmd)
        cmd_in = open("client.pickle", "rb")

        while True:
            chunk = cmd_in.read(1024)
            if chunk:
                self.hash_val.update(chunk)
            else:
                hex_hash = self.hash_val.hexdigest()
                break

        return hex_hash

    def close_conn(self):
        self.client.close()

    def cmd_and_hash(self):
        cmd = self.write_single_coil()
        hash = self.serialize_cmd(cmd)
        return cmd, hash


if __name__ == '__main__':
    transaction = ModbusTransaction()
    transaction.establish_conn()
    # modbus_cmd = transaction.write_single_coil()
    # print(modbus_cmd)
    # digest = transaction.serialize_cmd(modbus_cmd)
    # print(digest)
    print(transaction.cmd_and_hash())
    results = transaction.read_single_coil()
    print(results.bits[0])
    transaction.close_conn()

import dis
import re
import sys

from io import StringIO
from client import Client
from server import Server


class ClientVerifier:
    def __init__(self, client):
        s = StringIO()
        save_stdout = sys.stdout
        sys.stdout = s
        dis.dis(client)
        sys.stdout = save_stdout
        got = s.getvalue()

        lines = got.split('\n')
        lines = [line.rstrip() for line in lines]

        unacceptable_methods = 'accept|listen'
        required_finded = dict.fromkeys(['socket', 'AF_INET', 'SOCK_STREAM'], False)
        
        for line in lines:
            result = re.search(f"LOAD_METHOD(\s+)(\d+)(\s)\(({unacceptable_methods})\)", line)
            if result:
                raise AttributeError(f"class {client} has unacceptable method: {result.group(4)}")

            delimiter = '|'
            result = re.search(f"LOAD_GLOBAL(\s+)(\d+)(\s)\(({delimiter.join(required_finded.keys())})\)", line)
            if result:
                required_finded[result.group(4)] = True

        for key, item in required_finded.items():
            if item == False:
                raise AttributeError(f"class {client} has not required {key}")

        print(f'{client} - OK')

class ServerVerifier:
    def __init__(self, server):
        s = StringIO()
        save_stdout = sys.stdout
        sys.stdout = s
        dis.dis(server)
        sys.stdout = save_stdout
        got = s.getvalue()

        lines = got.split('\n')
        lines = [line.rstrip() for line in lines]

        unacceptable_methods = 'connect'
        required_finded = dict.fromkeys(['socket', 'AF_INET', 'SOCK_STREAM'], False)
        
        for line in lines:
            result = re.search(f"LOAD_METHOD(\s+)(\d+)(\s)\(({unacceptable_methods})\)", line)
            if result:
                raise AttributeError(f"class {server} has unacceptable method: {result.group(4)}")

            delimiter = '|'
            result = re.search(f"LOAD_GLOBAL(\s+)(\d+)(\s)\(({delimiter.join(required_finded.keys())})\)", line)
            if result:
                required_finded[result.group(4)] = True

        for key, item in required_finded.items():
            if item == False:
                raise AttributeError(f"class {server} has not required {key}")

        print(f'{server} - OK')
            

if __name__ == "__main__":
    client_verifier = ClientVerifier(Client)
    server_verifier = ServerVerifier(Server)

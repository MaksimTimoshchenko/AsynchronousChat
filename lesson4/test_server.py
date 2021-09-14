import json
import sys
import time
import unittest
from socket import *

sys.path.append('../lesson3')
import server as server_module


class TestServer(unittest.TestCase):
    def test_init_server(self):
        try:
            addr = '0.0.0.0'
            port = 7777
            server_module.init_server(addr, port)
        except:
            self.fail("Test Error: server was not initialized!")

    def test_get_recieved_message(self):
        msg_data = {
            "action": "presence",
            "time": int(time.time()),
            "type": "status",
            "user": {
                "account_name": "GeekBrains",
                "status": "I'm connected to you!"
            }
        }

        msg = json.dumps(msg_data)
        chunk = msg.encode('utf-8')

        r = server_module.get_recieved_message(chunk)
        self.assertEqual(r, msg_data)


if __name__ == '__main__':
    unittest.main()

import json
import sys
import unittest
from socket import *

sys.path.append('../lesson3')
import client as client_module


class TestServer(unittest.TestCase):    
    def test_init_connection(self):
        try:
            addr = '127.0.0.1'
            port = 7777
            client_socket = client_module.init_connection(addr, port)
            client_module.send_presence_message(client_socket)
        except:
            self.fail("Test Error: server was not initialized!")

    def test_send_presence_message(self):
        addr = '127.0.0.1'
        port = 7777
        client_socket = client_module.init_connection(addr, port)
        try:
            client_module.send_presence_message(client_socket)
        except:
            self.fail("Test Error: message was not sent!")

    def test_get_recieved_message(self):
        msg_data = {
            "response": 200,
            "alert":"Соединение установлено!"
        }

        msg = json.dumps(msg_data)
        chunk = msg.encode('utf-8')

        r = client_module.get_recieved_message(chunk)
        self.assertEqual(r, msg_data)


if __name__ == '__main__':
    unittest.main()

import getopt, sys
import json
import time
import uuid

from log.client_log_config import client_logger
from socket import *
from threading import Thread


class Client:
    siska = socket(AF_INET, SOCK_STREAM)

    def __init__(self, address, port, mode, account_name):
        self.address = address
        self.port = port
        self.mode = mode
        self.socket = self.init_connection()
        self.account_name = account_name

    def init_connection(self):
        client_logger.info(f'Executed: init_connection({self.address=}, {self.port=})')
        try:
            s = socket(AF_INET, SOCK_STREAM)
            s.connect((self.address, self.port))
        except:
            client_logger.critical(f'Executed: init_connection({self.address=}, {self.port=}) with Exception: Connection to server failed')

        return s

    def connect(self): 
        if mode == 'r':
            self.reciever()
        elif mode == 'e':
            self.requestor()
        else:
            self.account_name = input('Введите свой логин: ')
            self.send_presence_message()

            t1 = Thread(target=self.reciever)
            t2 = Thread(target=self.requestor)
            t1.start()
            t2.start()

    def send_presence_message(self):    
        msg_data = {
            "action": "presence",
            "time": int(time.time()),
            "type": "status",
            "user": {
                "account_name": self.account_name,
                "status": "Connected to chat!"
            }
        }

        msg = json.dumps(msg_data)
        sent = self.socket.send(msg.encode('utf-8'))

        if sent == 0:
            client_logger.critical(f'Executed: send_presence_message({self.socket=}) with Error: Socket connection broken')
            raise RuntimeError("Socket connection broken")

    def get_recieved_message(self):
        try:
            chunk = self.socket.recv(1000000)
            server_response = json.loads(chunk.decode('utf-8'))
            return server_response
        except Exception as ex:
            pass

    def reciever(self):
        while True:
            data = self.get_recieved_message()
            if data and data['action'] == 'message':
                print(f"\n{data['user']['account_name']} написал: {data['message']}\nВаше сообщение: ", end="")

    def requestor(self):
        while True:
            msg = input('Ваше сообщение: ')
            msg_data = {
                "action": "message",
                "time": int(time.time()),
                "type": "status",
                "user": {
                    "account_name": self.account_name,
                },
                "message": msg
            }

            msg = json.dumps(msg_data)

            try:
                self.socket.send(msg.encode('utf-8'))
            except Exception:
                client_logger.critical(f'Failed to send message')

def main(address, port, mode, account_name):
    client = Client(address, port, mode, account_name)
    client.connect()


if __name__ == '__main__':
    try:
        opts, args = getopt.getopt(sys.argv[1:], "a:p:m:u:", ["address=", "port=", "username="])
        address = ''
        port = 7777
        account_name = uuid.uuid4().hex[:6].upper()
        mode = 'd'
        verbose = False
        for o, a in opts:
            if o in ("-a", "--address"):
                address = a
            elif o in ("-p", "--port"):
                port = int(a)
            elif o in ("-m", "--mode"):
                mode = a
            elif o in ("-u", "--username"):
                account_name = a
            else:
                assert False, "Unhandled option"

        if address:
            main(address=address, port=port, mode=mode, account_name=account_name)
        else:
            client_logger.critical(f'Failed to start client: error while getting options')
            print('main.py -a <addr:str> -p <port:int>')
            sys.exit(2)
    except getopt.GetoptError as err:
        client_logger.critical(f'Failed to start client: error while getting options')
        print('Error while getting options')
        sys.exit(2) 
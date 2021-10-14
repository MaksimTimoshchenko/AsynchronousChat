import getopt, sys
import json
import re
import time
import uuid

from log.client_log_config import client_logger
from socket import *
from threading import Thread
from tables import Contact
from storage import Storage, ClientStorage, ContactStorage


class Client:
    siska = socket(AF_INET, SOCK_STREAM)

    def __init__(self, address, port, mode, account_name):
        self.address = address
        self.port = port
        self.mode = mode
        self.socket = self.init_connection()
        self.account_name = account_name
        self.commands = ['get_contacts', 'add_contact', 'del_contact']
        self.server_responded = True

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
            if data:
                if 'action' in data and data['action'] == 'message':
                    print(f"\n{data['user']['account_name']} написал: {data['message']}\nВаше сообщение: ", end="")
                else:
                    print(f"{data}\n", end="")
                    self.server_responded = True

    def requestor(self):
        while True:
            if self.server_responded:
                entered_msg = input('Ваше сообщение: ')
                msg_data = self.handle_message(entered_msg)

                if msg_data is not None:
                    msg = json.dumps(msg_data)
                    try:
                        self.socket.send(msg.encode('utf-8'))
                        
                        if msg_data['action'] in self.commands:
                            self.server_responded = False
                    except Exception:
                        client_logger.critical(f'Failed to send message')

    def handle_message(self, entered_msg):
        msg_data = {
            "action": "message",
            "time": int(time.time()),
            "type": "status",
            "user": {
                "account_name": self.account_name,
            },
            "message": entered_msg
        }
        
        if entered_msg.startswith('/'):
            result = re.search(r'\/([\w\S]*)([\s]([\w\s]*))?', entered_msg)
            command = result.group(1)

            if command in self.commands:
                msg_data['action'] = command

                if command in ['add_contact', 'del_contact']:
                    contact_account_name = result.group(3)
                    msg_data['command_username'] = contact_account_name

                    if not contact_account_name:
                        print('Ошибка: пустой логин контакта!\nДля корректной работы команды необходимо ввести логин контакта через пробел после команды /add_contact|del_contact {логин_контакта}\n', end='')
                        return None

        return msg_data

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
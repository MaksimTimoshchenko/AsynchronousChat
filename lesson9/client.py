import getopt, sys
import json
import time
import uuid

from log.client_log_config import client_logger, log
from socket import *
from threading import Thread

@log
def connect_server(addr, port, mode, account_name): 
    s = init_connection(addr, port)
    
    if mode == 'r':
        reciever(s)
    elif mode == 'e':
        requestor(s, account_name)
    else:
        account_name = input('Введите свой логин: ')
        send_presence_message(s, account_name)

        t1 = Thread(target=reciever, args=(s, ))
        t2 = Thread(target=requestor, args=(s, account_name, ))
        t1.start()
        t2.start()

def init_connection(addr, port):
    client_logger.info(f'Executed: init_connection({addr=}, {port=})')
    try:
        s = socket(AF_INET,SOCK_STREAM)
        s.connect((addr, port))
    except:
        client_logger.critical(f'Executed: init_connection({addr=}, {port=}) with Exception: Connection to server failed')

    return s

def send_presence_message(s, account_name):    
    msg_data = {
        "action": "presence",
        "time": int(time.time()),
        "type": "status",
        "user": {
            "account_name": account_name,
            "status": "Connected to chat!"
        }
    }

    msg = json.dumps(msg_data)
    sent = s.send(msg.encode('utf-8'))

    if sent == 0:
        client_logger.critical(f'Executed: send_presence_message({s=}) with Error: Socket connection broken')
        raise RuntimeError("Socket connection broken")

def get_recieved_message(s):
    try:
        chunk = s.recv(1000000)
        server_response = json.loads(chunk.decode('utf-8'))
        return server_response
    except Exception as ex:
        pass

def reciever(s):
    while True:
        data = get_recieved_message(s)
        if data and data['action'] == 'message':
            print(f"\n{data['user']['account_name']} написал: {data['message']}\nВаше сообщение: ", end="")

def requestor(s, account_name):
    while True:
        msg = input('Ваше сообщение: ')
        msg_data = {
            "action": "message",
            "time": int(time.time()),
            "type": "status",
            "user": {
                "account_name": account_name,
            },
            "message": msg
        }

        msg = json.dumps(msg_data)

        try:
            s.send(msg.encode('utf-8'))
        except Exception:
            client_logger.critical(f'Failed to send message')



if __name__ == '__main__':
    try:
        opts, args = getopt.getopt(sys.argv[1:], "a:p:m:u:", ["address=", "port=", "username="])
        addr = ''
        port = 7777
        account_name = uuid.uuid4().hex[:6].upper()
        mode = 'd'
        verbose = False
        for o, a in opts:
            if o in ("-a", "--address"):
                addr = a
            elif o in ("-p", "--port"):
                port = int(a)
            elif o in ("-m", "--mode"):
                mode = a
            elif o in ("-u", "--username"):
                account_name = a
            else:
                assert False, "Unhandled option"

        if addr:
            connect_server(addr=addr, port=port, mode=mode, account_name=account_name)
        else:
            client_logger.critical(f'Failed to start client: error while getting options')
            print('main.py -a <addr:str> -p <port:int>')
            sys.exit(2)
    except getopt.GetoptError as err:
        client_logger.critical(f'Failed to start client: error while getting options')
        print('Error while getting options')
        sys.exit(2) 

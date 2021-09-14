from socket import *
import getopt, sys
import json
import time

def connect_server(addr, port): 
    s = init_connection(addr, port)
    send_presence_message(s)
    chunk = s.recv(1000000)
    get_recieved_message(chunk)
    s.close()

def init_connection(addr, port):
    try:
        s = socket(AF_INET,SOCK_STREAM)
        s.connect((addr, port))
    except:
        raise RuntimeError("Connection to server failed")

    return s

def send_presence_message(s):
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
    sent = s.send(msg.encode('utf-8'))

    if sent == 0:
        raise RuntimeError("Socket connection broken")

def get_recieved_message(chunk):
    if chunk == b'':
        raise RuntimeError("Socket connection broken")

    server_response = json.loads(chunk.decode('utf-8'))
    print(server_response)
    return server_response


if __name__ == '__main__':
    try:
        opts, args = getopt.getopt(sys.argv[1:], "a:p:", ["address=", "port="])
        addr = ''
        port = 7777
        verbose = False
        for o, a in opts:
            if o in ("-a", "--address"):
                addr = a
            elif o in ("-p", "--port"):
                port = a
            else:
                assert False, "Unhandled option"

        if addr:
            connect_server(addr, port)
        else:
            print('main.py -a <addr:str> -p <port:int>')
            sys.exit(2)
    except getopt.GetoptError as err:
        print('Error while getting options')
        sys.exit(2) 

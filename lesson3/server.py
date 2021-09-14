import getopt, sys
import json
from socket import *


def run(addr, port):
    s = init_server(addr, port)

    while True:
        client, _ = s.accept()

        chunk = client.recv(1000000)
        get_recieved_message(chunk)
        send_response_message(client)

        client.close()

def init_server(addr, port):
    try:
        s = socket(AF_INET,SOCK_STREAM)
        s.bind((addr, port))
        s.listen()
    except:
        raise RuntimeError("Connection to server failed")

    return s

def get_recieved_message(chunk):
    if chunk == b'':
        raise RuntimeError("Socket connection broken")

    client_request = json.loads(chunk.decode('utf-8'))
    
    print(client_request)
    return client_request

def send_response_message(client):
    msg_data = {
        "response": 200,
        "alert":"Соединение установлено!"
    }
    msg = json.dumps(msg_data)
    sent = client.send(msg.encode('utf-8'))

    if sent == 0:
        raise RuntimeError("Socket connection broken")

if __name__ == '__main__':
    try:
        opts, args = getopt.getopt(sys.argv[1:], "a:p:", ["address=", "port="])
        addr = '0.0.0.0'
        port = 7777
        verbose = False
        for o, a in opts:
            if o in ("-a", "--address"):
                addr = a
            elif o in ("-p", "--port"):
                port = a
            else:
                assert False, "Unhandled option"

        run(addr, port)    
    except getopt.GetoptError as err:
        print('Error while getting options')
        sys.exit(2) 

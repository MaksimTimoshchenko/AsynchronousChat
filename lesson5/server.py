import getopt, sys
import json

from log.server_log_config import server_logger
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
    server_logger.info(f'Executed: init_server({addr=}, {port=})')
    try:
        s = socket(AF_INET,SOCK_STREAM)
        s.bind((addr, port))
        s.listen()
    except:
        server_logger.critical(f'Executed: init_server({addr=}, {port=}) with Exception: Failed to initialize server socket')
    return s

def get_recieved_message(chunk):
    server_logger.info(f'Executed: get_recieved_message({chunk=})')
    if chunk == b'':
        server_logger.critical(f'Executed: get_recieved_message({chunk=}) with Error: Socket connection broken')
        raise RuntimeError("Socket connection broken")

    client_request = json.loads(chunk.decode('utf-8'))
    
    print(client_request)
    return client_request

def send_response_message(client):
    server_logger.info(f'Executed: send_response_message({client=})')
    msg_data = {
        "response": 200,
        "alert":"Соединение установлено!"
    }
    msg = json.dumps(msg_data)
    sent = client.send(msg.encode('utf-8'))

    if sent == 0:
        server_logger.critical(f'Executed: send_response_message({client=}) with Error: Socket connection broken')
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
        server_logger.critical(f'Failed to start server: error while getting options')
        print('Error while getting options')
        sys.exit(2) 

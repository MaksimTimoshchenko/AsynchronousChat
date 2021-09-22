import getopt, sys
import json
from socket import *


def run(addr, port):
    s = socket(AF_INET, SOCK_STREAM)
    s.bind((addr, port))
    s.listen()


    while True:
        client, _ = s.accept()
        data = client.recv(1000000)
        client_request = json.loads(data.decode('utf-8'))
        print(client_request)

        msg_data = {
            "response": 200,
            "alert":"Соединение установлено!"
        }
        msg = json.dumps(msg_data)

        client.send(msg.encode('utf-8'))
        client.close()

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

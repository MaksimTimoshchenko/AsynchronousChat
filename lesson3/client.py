from socket import *
import getopt, sys
import json
import time

def connect_server(addr, port):
    s = socket(AF_INET,SOCK_STREAM)
    s.connect((addr, port))

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
    s.send(msg.encode('utf-8'))
    data = s.recv(1000000)
    server_response = json.loads(data.decode('utf-8'))
    print(server_response)
    s.close()

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

import getopt, sys
import json
import select

from log.server_log_config import server_logger, log
from socket import *

@log
def run(addr, port):
    s = init_server(addr, port)
    clients = []

    while True:
        try:
            connection, address = s.accept()
        except OSError as e:
            pass
        else:
            print("Получен запрос на соединение с %s" % str(address))
            clients.append(connection)
        finally:
            w, r = [], []
            try:
                r, w, e = select.select(clients, clients, [], 1)
            except Exception as e:
                pass
 
            requests = get_recieved_messages(r, clients)
            
            if requests:
                send_response_messages(requests, w, clients)

def init_server(addr, port):
    server_logger.info(f'Executed: init_server({addr=}, {port=})')
    try:
        s = socket(AF_INET, SOCK_STREAM)
        s.bind((addr, port))
        s.listen()
        s.settimeout(0.2)
    except:
        server_logger.critical(f'Executed: init_server({addr=}, {port=}) with Exception: Failed to initialize server socket')
    return s

def get_recieved_messages(r_clients, all_clients):
    responses = {}
    for s in r_clients:
        try:
            data = s.recv(1000000).decode('utf-8')
            responses[s] = data
        except Exception as ex:
            server_logger.critical('Клиент {} {} отключился'.format(s.fileno(), s.getpeername()))
            all_clients.remove(s)
    return responses

def send_response_messages(requests, w_clients, all_clients):
   for s in w_clients:
       if s in requests:
           try:
               response = s.encode('utf-8')
               s.send(response)
           except:
               server_logger.critical('Клиент {} {} отключился'.format(s.fileno(), s.getpeername()))
               s.close()
               all_clients.remove(s)

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

        run(addr=addr, port=port)    
    except getopt.GetoptError as err:
        server_logger.critical(f'Failed to start server: error while getting options')
        print('Error while getting options')
        sys.exit(2) 

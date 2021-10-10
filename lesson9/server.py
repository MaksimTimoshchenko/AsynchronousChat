import getopt, sys, json, select, re

from log.server_log_config import server_logger, log
from socket import *

@log
def run(addr, port):
    s = init_server(addr, port)
    clients = {}
    clients_connections = []

    while True:
        try:
            connection, address = s.accept()
        except OSError as e:
            pass
        else:
            print("Получен запрос на соединение с %s" % str(address))
            clients_connections.append(connection)
        finally:
            w, r = [], []
            try:
                r, w, e = select.select(clients_connections, clients_connections, [], 1)
            except Exception as e:
                pass
 
            requests = get_recieved_messages(r, clients_connections, clients)
            if requests:
                send_response_messages(requests, w, clients_connections, clients)

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

def get_recieved_messages(r_clients, clients_connections, clients):
    responses = {}
    for s in r_clients:
        try:
            data = json.loads(s.recv(1000000).decode('utf-8'))
            responses[s] = data

            if data["action"] == "presence":
                clients[s] = data["user"]["account_name"]
            
        except Exception:
            server_logger.critical('Client {} {} disconnected'.format(s.fileno(), s.getpeername()))
            s.close()
            clients_connections.remove(s)
            del clients[s]
    return responses

def send_response_messages(requests, w_clients, clients_connections, clients):
    for s in w_clients:
        try:
            for request in requests.values():
                try:
                    if request["user"]["account_name"] != clients[s]:
                        if request["message"].startswith('@'):
                            result = re.search(r'\@([\w\S]*)([\w\s\S]*)', request["message"])
                            message_recipient = result.group(1)
                            # message_text = result.group(2)

                            if message_recipient == clients[s]:
                                # request["message"] = message_text
                                response = json.dumps(request).encode('utf-8')
                                s.send(response)
                        else:
                            response = json.dumps(request).encode('utf-8')
                            s.send(response)
                except:
                    pass
        except Exception:
                server_logger.critical('Client {} {} disconnected'.format(s.fileno(), s.getpeername()))
                s.close()
                clients_connections.remove(s)
                del clients[s]

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

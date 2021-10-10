import getopt
import json
import re
import select
import sys

from log.server_log_config import server_logger
from PortDescriptor import PortDescriptor
from socket import *


class Server:
    port = PortDescriptor("port")
    
    def __init__(self, address, port):
        self.address = address
        self.port = port
        self.socket = self.init_socket()
        self.clients = {}
        self.clients_connections = []

    def init_socket(self):
        server_logger.info(f'Executed: init_socket({self.address=}, {self.port=})')
        try:
            s = socket(AF_INET, SOCK_STREAM)
            s.bind((self.address, self.port))
            s.listen()
            s.settimeout(0.2)
        except:
            server_logger.critical(f'Executed: init_socket({self.address=}, {self.port=}) with Exception: Failed to initialize server socket')
        return s

    def run(self):
        while True:
            try:
                connection, address = self.socket.accept()
            except OSError as e:
                pass
            else:
                print("Получен запрос на соединение с %s" % str(address))
                self.clients_connections.append(connection)
            finally:
                w, r = [], []
                try:
                    r, w, e = select.select(self.clients_connections, self.clients_connections, [], 1)
                except Exception as e:
                    pass
    
                requests = self.get_recieved_messages(r)
                if requests:
                    self.send_response_messages(requests, w)
        
    def get_recieved_messages(self, r_clients):
        responses = {}
        for s in r_clients:
            try:
                data = json.loads(s.recv(1000000).decode('utf-8'))
                responses[s] = data

                if data["action"] == "presence":
                    self.clients[s] = data["user"]["account_name"]
                
            except Exception:
                server_logger.critical('Client {} {} disconnected'.format(s.fileno(), s.getpeername()))
                s.close()
                self.clients_connections.remove(s)
                del self.clients[s]
        return responses

    def send_response_messages(self, requests, w_clients):
        for s in w_clients:
            try:
                for request in requests.values():
                    try:
                        if request["user"]["account_name"] != self.clients[s]:
                            if request["message"].startswith('@'):
                                result = re.search(r'\@([\w\S]*)([\w\s\S]*)', request["message"])
                                message_recipient = result.group(1)
                                # message_text = result.group(2)

                                if message_recipient == self.clients[s]:
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
                    self.clients_connections.remove(s)
                    del self.clients[s]

def main(address, port):
    server = Server(address, port)
    server.run()

if __name__ == '__main__':
    try:
        opts, args = getopt.getopt(sys.argv[1:], "a:p:", ["address=", "port="])
        address = '0.0.0.0'
        port = 7777
        verbose = False
        for o, a in opts:
            if o in ("-a", "--address"):
                address = a
            elif o in ("-p", "--port"):
                port = int(a)
            else:
                assert False, "Unhandled option"

        main(address=address, port=port)    
    except getopt.GetoptError as err:
        server_logger.critical(f'Failed to start server: error while getting options')
        print('Error while getting options')
        sys.exit(2)
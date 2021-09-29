from socket import *


def echo_client():
    with socket(AF_INET, SOCK_STREAM) as sock:
        sock.connect(('127.0.0.1', 7777))
        while True:
            data = sock.recv(1000000).decode('utf-8')
            if data:
                print('Ответ:', data)


if __name__ == '__main__':
    echo_client()
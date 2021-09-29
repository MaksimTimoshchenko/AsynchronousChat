from socket import *


def echo_client():
    with socket(AF_INET, SOCK_STREAM) as sock:
        sock.connect(('127.0.0.1', 7777))
        while True:
            msg = input('Ваше сообщение: ')
            if msg:
                sock.send(msg.encode('utf-8'))


if __name__ == '__main__':
    echo_client()
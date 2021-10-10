import ipaddress
import re
import socket
import subprocess

from tabulate import tabulate


# Задание 1
def host_ping(host_list, with_print=True):

    host_result = {'Reachable': [], 'Unreachable': []}
    subprocess_ping = ''
    for host in host_list:
        ipv4 = ''
        try:
            ipv4 = ipaddress.ip_address(host)
        except Exception as ex:
            pass

        try:
            ipv4 = ipaddress.ip_address(socket.gethostbyname(host))
        except Exception as ex:
            pass

        args = ['ping', '-c', '1', str(ipv4)]
        try:
            subprocess_ping = subprocess.Popen(args, stdout=subprocess.PIPE)
        except Exception:
            pass
        else:
            subprocess_ping_output = subprocess_ping.stdout.read().decode('utf-8')
            result = re.search('1 received', subprocess_ping_output)
            if result:
                if(with_print):
                    print(f'{host} узел доступен')
                host_result['Reachable'].append(host)
            else:
                if(with_print):
                    print(f'{host} узел недоступен')
                host_result['Unreachable'].append(host)
                
    return host_result

host_list = ['stackoverflow.com', 'google.com', '127.0.0.1', '192.168.1.1', '192.168.1.255']
host_ping(host_list)


# Задание 2
def host_range_ping(ip_range, with_print=True):
    try:
        ip_network = ipaddress.ip_network(ip_range)
    except Exception as e:
        print(e)
    else:
        host_list = [ip_address for ip_address in ip_network]
        return host_ping(host_list, with_print)

host_range_ping('127.0.0.0/29')


# Задание 3
def host_range_ping_tab(ip_range):
    host_result = host_range_ping(ip_range, False)
    print(tabulate(host_result, headers="keys"))

host_range_ping_tab('127.0.0.0/29')


# Задание 4
def run_clients(count_recievers, count_requestors):
    address = '127.0.0.1'

    for i in range(count_recievers):
        print(1)
        p = subprocess.Popen([f'python3 client.py -a {address} -m r -u UserReciever{i}'],
        shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = p.communicate()

    for i in range(count_requestors):
        print(2)
        p = subprocess.Popen([f'python3 client.py -a {address} -m e -u UserRequestor{i}'],
        shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        message = b"Hello world!"
        output, error = p.communicate(message)
        print(output.decode())

run_clients(count_recievers=2, count_requestors=2)
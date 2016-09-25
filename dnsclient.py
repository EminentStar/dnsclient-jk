import socket
import sys


PORT = 53


def get_ip_addr(host):
    return '202.179.177.22'


def get_local_dns_ip():
    f = open('/etc/resolv.conf', 'r')
    local_dns = ''
    while True:
        line = f.readline()
        if 'nameserver' in line:
            local_dns = line.split()[1]
            break
    return local_dns


get_ip_addr('www.naver.com')


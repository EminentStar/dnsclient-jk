import socket
import sys
from DNSHeader import DNSHeader
from DNSQuestionSection import DNSQuestionSection


PORT = 53


def dns_query(host):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    except socket.error:
        print('소켓 생성 에러')
        sys.exit()

    query_header = DNSHeader()



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


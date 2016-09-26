import socket
import sys
from DNSHeader import DNSHeader
from DNSQuestionSection import DNSQuestionSection


PORT = 53


def dns_query():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    except socket.error:
        print('소켓 생성 에러')
        sys.exit()

    seed_host = sys.argv[1]
    query_host = sys.argv[2] 

    query_header = DNSHeader(0,1,1,0,0,0)
    question_section = DNSQuestionSection(query_host, 1, 1)
    

    target = (seed_host, PORT)
    
    query = query_header.to_bytes() + question_section.to_bytes()
    
    try:
        s.sendto(query, target)
        
        # TC에 대응하여 TCP 송신을 구현할 것인가??
        response = s.recvfrom(1024)
        print(response)
    except (socket.error, msg):
        print('Error Code: %s Message: %s' % (msg[0], msg[1]))
        sys.exit()


def get_local_dns_ip():
    f = open('/etc/resolv.conf', 'r')
    local_dns = ''
    while True:
        line = f.readline()
        if 'nameserver' in line:
            local_dns = line.split()[1]
            break
    return local_dns


dns_query()

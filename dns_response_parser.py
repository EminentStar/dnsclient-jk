
def dns_response_parser(msg):
    did = msg[:2]
    flags = msg[2:4]
    qdcount = two_bytes_to_int(msg[4:6])
    ancount = two_bytes_to_int(msg[6:8])
    nscount = two_bytes_to_int(msg[8:10])
    arcount = two_bytes_to_int(msg[10:12])
    
    sections = msg[12:]

    print(did)
    print(flags)
    print(qdcount)
    print(ancount)
    print(nscount)
    print(arcount)
    print(sections)
    

def two_bytes_to_int(bytes):
    first = '{0:08b}'.format(int(bytes[0]))
    second = '{0:08b}'.format(int(bytes[1]))
    concated = first + second
    return int(concated, 2)
   

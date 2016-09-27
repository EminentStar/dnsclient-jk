import dns_response_parser


class DNSResourceRecord(object):
    """
    DNS Resource REcord 구조 

        <-----------------32 bits----------------->
        -------------------------------------------
                           Name
        -------------------------------------------
                Type        |       Class
        -------------------------------------------
                     Time To Live(TTL) 
        -------------------------------------------
        Resource Data Length|  Resource Data
        ---------------------
                        .................
        -------------------------------------------
       
       * DNS Common Resource Recourd Format
       -------------------------------------
       Field Name: Size(bytes): Description
       -------------------------------------
       Name: 가변: RR의성격에 맞는 객체나 도메인이나 zone을 포함한다. 
       Type: 2: RR의 타입을 나타내는 code value
       Class: 2: 요청되어진 RR의 클래스를 명시한다. 보통 1은 Internet("IN")
       TTL: 4: RR이 읽혀지는 장치에서의 캐시에서 다시 얻어져야하는 시간(초)를 명시한다.
       Resource Data Length(RDLength): 2: RData의 크기를 명시한다.(bytes)
       Resource Data(RData): 가변: RR의 데이터 부분이다.
        Type A 일 때: 32-bit IP address를 나타낸다.
    """
    def __init__(self, name, type, cls, ttl, rdlen, rdata):
        self.name = self.bytes_to_name(name)
        self.type = self.bytes_to_type(type)
        self.cls = self.bytes_to_cls(cls)
        self.ttl = dns_response_parser.four_bytes_to_int(ttl)
        self.rlden = dns_response_parser.two_bytes_to_int(rdlen)
        self.rdata = self.bytes_to_rdata(self.type, rdata)
    
    
    def bytes_to_type(self, type_bytes):
        type_int = dns_response_parser.two_bytes_to_int(type_bytes)
        typeMap = {
                '1': 'A',
                '2': 'NS',
                '5': 'CNAME'
                }
        return typeMap.get(str(type_int))
    

    def bytes_to_cls(self, cls_bytes):
        cls_int = dns_response_parser.two_bytes_to_int(cls_bytes)
        clsMap = {
                '1': 'IN'
                }
        return clsMap.get(str(cls_int))


    def bytes_to_name(self, bytes):
        name = ''
        chunk_len = bytes[0]
        idx = 1
        bytes_len = len(bytes)

        while idx < bytes_len:
            if chunk_len == 0:
                chunk_len = bytes[idx]
                if chunk_len != 0:
                    name += '.'
            else:
                name += chr(bytes[idx])
                chunk_len -= 1
            idx += 1
        
        return name


    def bytes_to_ipaddr(self, bytes):
        ipaddr = ''
        for part in bytes:
            ipaddr += str(part) + '.'

        ipaddr = ipaddr[:-1] # 마지막 dot 제거
        return ipaddr


    def bytes_to_rdata(self, type, bytes):
        rval = ''
        if type == 'A': # A type data
            rval = self.bytes_to_ipaddr(bytes)
        else:
            rval = self.bytes_to_name(bytes)
        return rval

    
    def to_string(self):
       print("%-25s %5s %7s %-5s %s" % (self.name, self.ttl, self.cls, self.type, self.rdata)) 

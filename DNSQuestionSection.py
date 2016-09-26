import struct

class DNSQuestionSection(object):
    """
    DNS Question Section 구조 

        <-----------------16 bits----------------->
        -------------------------------------------
                           QNAME
                            ...
        -------------------------------------------
                           QTYPE 
        -------------------------------------------
                           QCLASS 
        -------------------------------------------
    """

    def __init__(self, name, type, cls):
        self.set_qname(name)
        self.set_qtype(type)
        self.set_qclass(cls)
        
    
    def set_qname(self, name):
        self.qname = self.construct_qname(name)


    def get_qname(self):
        return self.qname
    

    def set_qtype(self, type):
        """
            qtype은 unsigned 16 bit 값이다.

            value: Meaning/Use
            -------------------------------------
            x'0001 (1): A type record를 요청한다.
            x'0002 (2): NS type record를 요청한다.
            x'0005 (5): CNAME type record를 요청한다.
            x'0006 (6): SOA type record를 요청한다.
            ...
            ...
        """
        self.qtype = struct.pack('>H', type)

    
    def set_qclass(self, cls):
        """
            qclass는 unsigned 16 bit 값이다.

            요청되어지는 RR의 class를 명시한다. 
            보통 Internet;'IN'을 의미하는 1이 사용된다.
            
            x'0001 (1): IN or Internet
        """
        self.qclass = struct.pack('>H', cls)


    def to_bytes(self):
        qsection = self.qname + self.qtype + self.qclass
        return qsection


    def construct_qname(self, name):
        """
            '.'을 딜리미터로 name을 split한다.
            loop를 돌면서 [length][characters]...[0]의 형태의 encoding된 qname을 형성한다.
        """
        parts = name.split('.')
        qname = b''

        for part in parts:
            qname += struct.pack('>b', len(part))
            qname += part.encode()
        
        qname += struct.pack('>b', 0)
        return qname
    


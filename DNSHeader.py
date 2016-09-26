import random
import struct
import bitarray


class DNSHeader(object):
    """
        DNS Header 구조(총 12 Bytes)

        <-----------------16 bits----------------->
        -------------------------------------------
                            ID
        -------------------------------------------
        QR | Opcode | AA | TC | RD | RA | Z | RCODE
        -------------------------------------------
                          QDCOUNT
        -------------------------------------------
                          ANCOUNT
        -------------------------------------------
                          NSCOUNT
        -------------------------------------------
                          ARCOUNT
        -------------------------------------------

    """
    def __init__(self, opcode, recursive_desired, qd_count, an_count, ns_count, ar_count):
        self.set_did()        
        self.set_dor()
        self.set_opcode(opcode)
        self.set_aa()
        self.set_tc()
        self.set_rd(recursive_desired)
        self.set_ra()
        self.set_z()
        self.set_rcode()
        self.set_counts(qd_count, an_count, ns_count, ar_count)


    def set_did(self):
        randnum = int(random.uniform(-32768, 32768))
        self.did = struct.pack('>h', randnum)

    
    def set_dor(self):
        """
            OR 플래그는 1 bit이며, 
            0이면 query, 1이면 response로 메시지를 구분한다.
        """
        self.dor = bitarray.bitarray([0])
    

    def set_opcode(self, opcode):
        """
            Opcode 플래그는 메시지가 운반하는 쿼리의 타입을 명세화한다.
            
            4 bit로 구성되며, 
            쿼리의 생성자에 의해 세팅되고 응답에서는 쿼리의 값이 복사된다.
            
            Opcode Value: Query Name: Description
            ---------------------------------------------------
            0: QUERY: 표준 쿼리
            1: IQUERY: 인벌스 쿼리;사용되지않음.
            2: STATUS: 
            3: (reserve): 예약되었지만 사용X.
            4: NOTIFY: 원서버가 두번째 서버에게 zone이 바뀌었고 
                       zone을 변경하라고 요청하도록 하는 메시지.
            5: UPDATE: DDNS를 구현하기 위해 생김.
                       이것은 Resource Records(RR) 가
                       선택적으로 추가, 삭제, 수정되는 것을 
                       허락한다.
        """
        opcode_str = '{0:04b}'.format(opcode)
        bit_list = self.str_to_bitlist(opcode_str)
        self.opcode = bitarray.bitarray(bit_list)


    def set_aa(self):
        """
            aa 플래그는 1 bit으로 구성되며,
            Authoritative Answer의 약자로,
            1로 설정되면, 응답을 생성한 서버가 Question 섹션이 위치한
            도메인이 있는 zone의 Authoritative임을 가리킨다.
            
            0이면 응답은 non-authoritative이다.
        """
        self.aa = bitarray.bitarray([0])
    
    
    def set_tc(self):
        """
            tc 플래그는 1 bit으로 구성되며,
            Truncation의 약자로,
            1로 설정되면 메시지가 truncated되었음을 알려준다.
            truncated된 이유로는 메시지의 길이가 transport mechanism의
            최대 길이보다 길기 때문이다.
            TCP는 보통 길이 제한을 두지않지만, 
            UDP 메시지는 512 bytes로 제한이 있다.
            그래서 클라이언트는 TCP세션을 통해 전체 메시지를 받을 필요가 있다.
        """
        self.tc = bitarray.bitarray([0])


    def set_rd(self,recursive_desired):
        """
          rd 플래그는 1 bit으로 구성되며, 
          Recursion Desired의 약자로,
          이것이 쿼리에서 설정되면, 쿼리를 받는 서버가 
          recursive resolution을 지원할때 쿼리에 대해 recursive하게 응답하도록
          요청한다. 
          이 플래그는 응답에서 값이 바뀌지 않는다.
        """
        if recursive_desired == 1:
            self.rd = bitarray.bitarray([1])
        elif recursive_desired == 0:
            self.rd = bitarray.bitarray([0])


    def set_ra(self):
        """
            ra 플래그는 1 bit로 구성되며, 
            Recursion Available의 약자로,
            응답을 생성하는 서버가 recursive query를 지원하면 응답에서 1로 설정되고
            그게 아니라면 0으로 설정된다. 이는 쿼리를 보낸 기기가 나중을 대비하여 
            고려할 수 있다.
        """
        self.ra = bitarray.bitarray([0])


    def set_z(self):
        """
            z는 3 bit로 구성되며,
            Zero의 약자로 0으로 설정되도록 되어있다.
        """
        self.z = bitarray.bitarray([0, 0, 0])


    def set_rcode(self):
        """
            rcode는 4 bit로 구성되며,
            response code의 약자로,
            쿼리에서는 0으로 설정된다.
            
            그후에 쿼리의 처리결과를 서버에서 응답을 보내면서 값이 바뀐다.
            이 플래그는 쿼리가 올바른 응답을 얻었는지,
            아니면 어떤 에러가 발생했는지를 알려준다.
            
            RCode Value: Response Code: Description
            ---------------------------------------
            0: No Error: 에러 발생X
            1: Format Error: 쿼리 메시지 형성에 문제가 있어서 서버가 받을 수 없음
            2: Server Failure: 서버의 문제로 서버가 쿼리에 대해 응답할 수 없음.
            3: Name Error: 쿼리에서 정의된 이름이 존재하지 않는 도메인일 때.
                           이 코드는 authoritative 서버에 의해 사용될 수 있거나
                           negative caching을 구현한 캐시 서버에서 사용될 수 있다.
            4: Not Implemented: 쿼리의 타입이 서버에서 지원되지 않을 떄
            5: Refused: 서버가 정책적 이유나 기술적인 이유로 쿼리의 처리는 거절함.
            6: YX Domain: Name exists when it should not?? (COULDN'T figure out.)
                          존재해선 안되는 도메인 네임이 존재할 떄?
            7: YX RR Set: 존재해선 안되는 RR set이 존재할 때?
            8: NX RR Set: 존재해야만 하는 RR set이 없을 떄
            9: Not Auth: 쿼리를 받는 서버가 명시된 zone을 위한 authoritative가 아닐 때. 
            10: Not Zone: 메시지의 name이 메시지의 zone안에 있지 않을 때
            
        """
        self.rcode = bitarray.bitarray([0, 0, 0, 0])


    def set_flags(self):
        bitarray_flags = self.dor + self.opcode + self.aa + self.tc + self.rd + self.ra + self.z + self.rcode
        self.flags = bitarray_flags.tobytes()


    def set_counts(self, qd_count, an_count, ns_count, ar_count):
        self.counts = struct.pack('>h', qd_count)
        self.counts += struct.pack('>h', an_count)
        self.counts += struct.pack('>h', ns_count)
        self.counts += struct.pack('>h', ar_count)
         

    def to_bytes(self):
        self.set_flags()
        return self.did + self.flags + self.counts

    
    def get_flags(self):
        return self.flags

    
    def get_counts(self):
        return self.counts


    def str_to_bitlist(self, str):
        str_list = list(str)
        int_list = []
        for chr in str_list:
           int_list.append(int(chr))
        return int_list 


import struct

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

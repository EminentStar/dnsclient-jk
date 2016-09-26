from enum import Enum
import struct


class RRHeader(Enum):
    name = 0
    type = 1
    cls = 2
    ttl = 3
    resource_data_len = 4
    resource_data = 5


def dns_response_parser(msg):
    did = msg[:2]
    flags = msg[2:4]
    qdcount = two_bytes_to_int(msg[4:6])
    ancount = two_bytes_to_int(msg[6:8])
    nscount = two_bytes_to_int(msg[8:10])
    arcount = two_bytes_to_int(msg[10:12])
    
    sections = msg[12:]
    
    """
    print(did)
    print(flags)
    print(qdcount)
    print(ancount)
    print(nscount)
    print(arcount)
    print(sections)
    """

    get_resource_records(msg, qdcount, ancount, nscount, arcount)


def parse_qd_list(msg, qdcount):
    qd_loop_count = qdcount
    
    qd_list = []

    data = b''
    idx = 12
    part_order = 0

    while qd_loop_count:
        if RRHeader(part_order) == RRHeader.name:
            data += struct.pack('>B', msg[idx])
            if msg[idx] == 0:
                data += b' '
                part_order += 1
            idx += 1
        elif RRHeader(part_order) == RRHeader.type:
            data += msg[idx: idx + 2] + b' '
            part_order += 1
            idx += 2
        elif RRHeader(part_order) == RRHeader.cls:
            data += msg[idx: idx + 2]
            part_order = 0
            idx += 2
            copy_data = data[:]
            qd_list.append(copy_data)
            data = b''
            qd_loop_count -= 1

    return qd_list


def parse_an_list(msg, start_idx, ancount):
    an_list = []

    idx = start_idx
    part_order = 0
    msg_len = len(msg)

    data = b''

    while idx < msg_len:
        if RRHeader(part_order) == RRHeader.name:
            print(msg[idx])
            if is_comp_pointer(msg[idx]):
                location = get_pointer_reference_location(msg[idx: idx+2])
                data += get_compressed_name(msg, location)
                data += b' '
                part_order += 1
                idx += 2
            else:
                data += struct.pack('>B', msg[idx])
                if msg[idx] == 0:
                    data += b' '
                    part_order += 1
                idx += 1
        elif RRHeader(part_order) == RRHeader.type or RRHeader(part_order) == RRHeader.cls:
            data += msg[idx:idx+2] + b' '
            idx += 2
            part_order += 1
        elif RRHeader(part_order) == RRHeader.ttl:
            data += msg[idx: idx+4] + b' '
            idx += 4
            part_order += 1
        elif RRHeader(part_order) == RRHeader.resource_data_len:
            data += msg[idx: idx+2] + b' '
            rdlen = two_bytes_to_int(msg[idx: idx+2]) 
            idx += 2
            part_order += 1
        elif RRHeader(part_order) == RRHeader.resource_data:
            rdata = msg[idx: idx + rdlen]
            
            if rdata[len(rdata)-2] >= b'\xc0'[0]:
                location = get_pointer_reference_location(rdata[len(rdata)-2:])
                rdata = rdata[:len(rdata)-2] + get_compressed_name(msg, location)
            
            data += rdata
            copy_data = data[:]
            an_list.append(copy_data)
            idx += rdlen
            part_order = 0
            data = b''

    return an_list


def get_resource_records(msg, qdcount, ancount, nscount, arcount):
    """
        전체 메시지에서 question, answer RR을 파싱한다.
    """
    qd_list = parse_qd_list(msg, qdcount)
    ns_list = []
    ar_list = []

    print(qd_list)
    qd_len = len_of_str_list(qd_list) 
    an_list = parse_an_list(msg, 12 + qd_len, ancount)
    print(an_list)


def len_of_str_list(str_list):
    sum = 0
    for str in str_list:
        for part in str.split(b' '):
            sum += len(part)
    return sum

def is_comp_pointer(byte):
    """
        해당 바이트가 DNS Message Compression Pointer인지 검증한다.
    """
    return byte >= b'\xc0'[0] 
    

def get_pointer_reference_location(two_bytes):
    """
        해당 포인터가 가리키는 위치를 변환한다.
    """
    bits_1 = '{0:08b}'.format(int(two_bytes[0]))
    bits_2 = '{0:08b}'.format(int(two_bytes[1]))
    concated_bits = bits_1 + bits_2
    concated_bits = concated_bits[2:]
    return int(concated_bits, 2)


def get_compressed_name(msg, location):
    """
        copression된 name의 일부분을 반환한다.
    """
    compressed_name = b''
    idx = location

    while msg[idx] != 0:
        compressed_name += struct.pack('>B', msg[idx])
        idx += 1

    compressed_name += b'\x00'
    return compressed_name


def bytes_to_resource_record(bytes):
    """
        바이트로 묶여있는 RR을 올바른 형태의 RR로 변환한다.    
    """


def two_bytes_to_int(bytes):
    first = '{0:08b}'.format(int(bytes[0]))
    second = '{0:08b}'.format(int(bytes[1]))
    concated = first + second
    return int(concated, 2)
   

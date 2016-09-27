from enum import Enum
import struct

from DNSResourceRecord import DNSResourceRecord


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
    

def get_resource_records(msg, qdcount, ancount, nscount, arcount):
    """
        전체 메시지에서 question, answer RR을 파싱한다.
    """
    qd_list = parse_qd_list(msg, qdcount)
    ns_list = []
    ar_list = []

    qd_len = len_of_str_list(qd_list) 
    an_list = parse_an_list(msg, 12 + qd_len, ancount)
    flags_dict = parse_flags(msg[2:4])

    for key, value in flags_dict.items():
        print('%s: %s'%(key, value))

    an_rr_list = []
    for ans in an_list:
        an_rr_list.append(bytes_to_resource_record(ans))
    
    for ans in an_rr_list:
        ans.to_string()


def parse_flags(flags_bytes):
    flags_bits = two_bytes_to_bits(flags_bytes)
    flags_dict = {}
    
    flags_dict['qr'] = flags_bits[:1]
    flags_dict['opcode'] = flags_bits[1:5]
    flags_dict['aa'] = flags_bits[5:6]
    flags_dict['tc'] = flags_bits[6:7]
    flags_dict['rd'] = flags_bits[7:8]
    flags_dict['ra'] = flags_bits[8:9]
    flags_dict['z'] = flags_bits[9:12]
    flags_dict['rcode'] = flags_bits[12:]
    
    return flags_dict


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
             
            if is_comp_pointer(rdata[len(rdata)-2]):
                location = get_pointer_reference_location(rdata[len(rdata)-2:])
                rdata = rdata[:len(rdata)-2] + get_compressed_name(msg, location)
         
            data += rdata
            copy_data = data[:]
            an_list.append(copy_data)
            idx += rdlen
            part_order = 0
            data = b''

    return an_list


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
        if is_comp_pointer(msg[idx]):
            sub_pointer_location = get_pointer_reference_location(msg[idx: idx+2])
            compressed_name += get_compressed_name(msg, sub_pointer_location)
            break;        

        compressed_name += struct.pack('>B', msg[idx])

        if msg[idx+1] == 0:
            compressed_name += b'\x00'
            break
        
        idx += 1
        

    return compressed_name


def bytes_to_resource_record(bytes):
    """
        바이트로 묶여있는 RR을 올바른 형태의 RR로 변환한다.
    """
    rr_parts = bytes.split(b' ')
    rr = DNSResourceRecord(rr_parts[0], rr_parts[1], rr_parts[2], rr_parts[3], rr_parts[4], rr_parts[5])

    return rr

def two_bytes_to_bits(bytes):
    first = '{0:08b}'.format(int(bytes[0]))
    second = '{0:08b}'.format(int(bytes[1]))
    concated = first + second
    return concated


def two_bytes_to_int(bytes):
    concated = two_bytes_to_bits(bytes)
    return int(concated, 2)


def four_bytes_to_int(bytes):
    first = two_bytes_to_bits(bytes[:2])
    second = two_bytes_to_bits(bytes[2:])
    concated = first + second
    return int(concated, 2)


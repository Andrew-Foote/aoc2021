from collections import namedtuple
from shared import register, main
from utils import product, digits, parse_digits

def parse(ip):
    line = next(ip).strip()
    ip.close()
    bindigits = []

    for c in line:
        hexdigit = int(c, 16)
        bindigits.extend(digits(hexdigit, 2, 4))

    return bindigits    

Packet = namedtuple('Packet', ['version', 'type_id', 'value', 'subpackets'])

def parse_version(src, i):
    version = parse_digits(src[i:i + 3], 2)
    return version, i + 3

def parse_type_id(src, i):
    type_id = parse_digits(src[i:i + 3], 2)
    return type_id, i + 3

def parse_literal(src, i):
    value = []

    while True:
        group = src[i:i + 5]
        value.extend(group[1:])
        i += 5

        if not group[0]:
            break

    return parse_digits(value, 2), i

def parse_length_type_id(src, i):
    return src[i], i + 1

def parse_subpackets_bit_length(src, i):
    return parse_digits(src[i:i + 15], 2), i + 15

def parse_subpacket_count(src, i):
    return parse_digits(src[i:i + 11], 2), i + 11

def parse_packet(src, i):
    version, i = parse_version(src, i)
    type_id, i = parse_type_id(src, i)
    subpackets = []

    if type_id == 4:
        value, i = parse_literal(src, i)
    else:
        value = None
        length_type_id, i = parse_length_type_id(src, i)

        if length_type_id:
            subpacket_count, i = parse_subpacket_count(src, i)

            for _ in range(subpacket_count):
                subpacket, i = parse_packet(src, i)
                subpackets.append(subpacket)
        else:
            subpackets_bit_length, i = parse_subpackets_bit_length(src, i)
            i0 = i

            while i - i0 < subpackets_bit_length:
                subpacket, i = parse_packet(src, i)
                subpackets.append(subpacket)

    return Packet(version, type_id, value, subpackets), i

def dfs(root, children):
    yield root

    for child in children(root):
        yield from dfs(child, children)

@register(day=16, level=1)
def level1(ip):
    bindigits = parse(ip)
    root_packet, i = parse_packet(bindigits, 0)
    packets = list(dfs(root_packet, lambda packet: packet.subpackets))
    return sum(packet.version for packet in packets)

def eval_(packet):
    if packet.type_id == 4:
        return packet.value
    elif packet.type_id == 0:
        return sum(map(eval_, packet.subpackets))
    elif packet.type_id == 1:
        return product(map(eval_, packet.subpackets))
    elif packet.type_id == 2:
        return min(map(eval_, packet.subpackets))
    elif packet.type_id == 3:
        return max(map(eval_, packet.subpackets))
    elif packet.type_id == 5:
        return 1 * (eval_(packet.subpackets[0]) > eval_(packet.subpackets[1]))
    elif packet.type_id == 6:
        return 1 * (eval_(packet.subpackets[0]) < eval_(packet.subpackets[1]))
    elif packet.type_id == 7:
        return 1 * (eval_(packet.subpackets[0]) == eval_(packet.subpackets[1]))

@register(day=16, level=2)
def level2(ip):
    bindigits = parse(ip)
    root_packet, i = parse_packet(bindigits, 0)
    return eval_(root_packet)

main(__name__)
import ipaddress
import struct

from sympy import E

class IP:
  def __init__(self, buff=None):
    # see struct:  https://docs.python.org/ja/3/library/struct.html    
    header = struct.unpack('<BBHHHBBH4s4s', buff)
    self.ver = header[0] >> 4
    self.ihl = header[0] & 0xF

    self.tos = header[1]
    self.len = header[2]
    self.id = header[3]
    self.offset = header[4]
    self.ttl = header[5]
    self.protocol_num = header[6]
    self.sum = header[7]
    self.src = header[8]
    self.dst = header[9]

    # store ip address in variables by readable format
    self.src_address = ipaddress.ip_address(self.src)
    self.dst_address = ipaddress.ip_address(self.dst)

    # mapping protocol constant value to name
    self.protocol_map = {1: "ICMP", 6: "TCP", 17: "UDP"}
    try:
      self.protocol = self.protocol_map[self.protocol_num]
    except Exception as e:
      print('%s No protocol for %s' % (e, self.protocol_num))
      self.protocol = str(self.protocol_num)

class ICMP:
  def __init__(self, buff):
    header = struct.unpack('<BBHHH', buff)
    self.type = header[0]
    self.code = header[1]
    self.sum = header[2]
    self.id = header[3]
    self.seq = header[4]
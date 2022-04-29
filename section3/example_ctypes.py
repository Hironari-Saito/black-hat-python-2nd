from ctypes import *
import socket
import struct

class IP(Structure):
  _fields_ = [
    ("ver",          c_ubyte,   4), # 4bit unsigned char
    ("ihl",          c_ubyte,   4), # 4bit unsigned char
    ("tos",          c_ubyte,   8), # 1byte unsigned char
    ("len",          c_ushort, 16), # 2byte unsigned short
    ("id",           c_ushort, 16), # 2byte unsigned short
    ("offset",       c_ushort, 16), # 2byte unsigned short
    ("ttl",          c_ubyte,   8), # 1byte unsigned char
    ("protocol_num", c_ubyte,   8), # 1byte unsigned char
    ("sum",          c_ushort, 16), # 2byte unsigned short
    ("src",          c_uint32, 32), # 4byte unsigned int
    ("dst",          c_uint32, 32), # 4byte unsigned int
  ]

  def __new__(cls, socket_buffer=None):
    # store input buffer in structure
    return cls.from_buffer_copy(socket_buffer)

  def __init__(self, socket_buffer=None):
    # store ip address in variables by readable format
    self.src_address = socket.inet_ntoa(struct.pack("<L", self.src))
    self.dst_address = socket.inet_ntoa(struct.pack("<L", self.dst))

    # mapping protocol constant value to name
    self.protocol_map = {1: "ICMP", 6: "TCP", 17: "UDP"}
    try:
      self.protocol = self.protocol_map[self.protocol_num]
    except Exception as e:
      print('%s No protocol for %s' % (e, self.protocol_num))
      self.protocol = str(self.protocol_num)
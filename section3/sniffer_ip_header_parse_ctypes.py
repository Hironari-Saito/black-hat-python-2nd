from ctypes import *
import os
import socket
import struct
import sys

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

def sniff(host):
  if os.name == 'nt':
    socket_protocol = socket.IPPROTO_IP
  else:
    socket_protocol = socket.IPPROTO_ICMP

  sniffer = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket_protocol)
  sniffer.bind((host, 0))

  sniffer.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

  if os.name == 'nt':
    sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)

  try:
    while True:
      # read a packet
      raw_buffer = sniffer.recvfrom(65535)[0]
      # create IP struct from first 20byte buffer
      ip_header = IP(raw_buffer[0:20])
      # output detected protocol and host
      print('Protocol: %s %s -> %s' % (ip_header.protocol, ip_header.src_address, ip_header.dst_address))

  except KeyboardInterrupt:
    # if windows, disable promiscuous mode
    if os.name == 'nt':
      sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)
      sys.exit()
if __name__ == '__main__':
  if len(sys.argv) == 2:
    host = sys.argv[1]
  else:
    host = '10.0.2.15'
  sniff(host)

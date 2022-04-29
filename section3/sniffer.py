import socket
import os

# host listen ip address
HOST = '10.0.2.15'

def main():
  # create raw socket and bind public interface
  if os.name =='nt':
    socket_protocol = socket.IPPROTO_IP
  else:
    socket_protocol = socket.IPPROTO_ICMP

  sniffer = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket_protocol)
  sniffer.bind((HOST, 0))

  # include ip header in result of capture
  sniffer.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

  # if windows, enable promiscuous mode
  if os.name == 'nt':
    sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)

  # read single packet
  print(sniffer.recvfrom(65565))

  # if windows, disable promiscuous mode
  if os.name == 'nt':
    sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)

if __name__ == '__main__':
  main()


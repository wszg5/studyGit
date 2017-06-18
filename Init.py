import socket
import sys

from struct import unpack

HOST = ''  # Symbolic name meaning all available interfaces
PORT = 1443  # Arbitrary non-privileged port

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print 'Socket created'

try:
    s.bind((HOST, PORT))
except socket.error, msg:
    print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()

print 'Socket bind complete'

s.listen(10)
print 'Socket now listening'

# wait to accept a connection - blocking call
conn, addr = s.accept()

# display client information
print 'Connected with ' + addr[0] + ':' + str(addr[1])

packet = conn.recvfrom(65565)
packet = packet[0]
ip_header = packet[0:20]
iph = unpack('!BBHHHBBH4s4s', ip_header)

s_addr = socket.inet_ntoa(iph[8])
d_addr = socket.inet_ntoa(iph[9])

version_ihl = iph[0]

version = version_ihl >> 4
ihl = version_ihl & 0xF
iph_length = ihl * 4
ttl = iph[5]
protocol = iph[6]
s_addr = socket.inet_ntoa(iph[8])
d_addr = socket.inet_ntoa(iph[9])

print(version_ihl)
print(version)
print(ihl)
print(ttl)
print(protocol)
print(s_addr)
print(d_addr)
conn.close()
s.close()

import socket

s = socket.socket()
host = socket.gethostname()
Port = 12345

s.connect((host,Port))
print(s.recv(1024))
s.close()

from socket import *


ADDR = ('0.0.0.0',7777)

s = socket()

s.connect(ADDR)

you = input('>>')

s.send(you.encode())

data = s.recv(32).decode()
print(data)


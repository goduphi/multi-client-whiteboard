import socket
import threading


class ReceiveThread(threading.Thread):
    def __init__(self, sock):
        threading.Thread.__init__(self)
        self.sock = sock

    def run(self):
        while True:
            print("Enter chat: ")
            message = input()
            self.sock.send(bytes(message, 'utf-8'))


s = socket.socket()
host = socket.gethostname()
port = 1100

s.connect((host, port))

t = ReceiveThread(s)
t.start()

while True:
    print(s.recv(1024))

t.join
s.close()
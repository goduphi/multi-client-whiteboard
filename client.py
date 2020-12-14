import socket
import threading


class ReceiveThread(threading.Thread):
    def __init__(self, sock):
        threading.Thread.__init__(self)
        self.sock = sock

    def run(self):
        while True:
            print("Enter chat: ", end="")
            message = input()
            self.sock.send(bytes(message, 'utf-8'))


# intialize all of the network code
# all the static code will be changed later
s = socket.socket()
host = socket.gethostname()
port = 1100
s.connect((host, port))

user = ReceiveThread(s)
user.start()

while True:
    print(s.recv(1024))

user.join
s.close()
import socket
import threading


class ReceiveThread(threading.Thread):
    def __init__(self, sock, sock_desp, clients):
        threading.Thread.__init__(self)
        self.sock = sock
        self.clients = clients
        self.message = None
        self.sock_desp = sock_desp

    def run(self):
        while True:
            print("Waiting to receive a message...")
            self.receive_message()

    def receive_message(self):
        self.message = self.sock_desp.recv(1024)
        print(f"Received message: {str(self.message)}")
        self.send_to_all_clients()

    def send_to_all_clients(self):
        for client in self.clients:
            client.send(self.message)


# 0 as the third arg means TCP
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
host = socket.gethostname()
port = 1100
s.bind((host, port))

s.listen(5)

clients = []
threads = []
client_id = 0

while True:
    sock_des, addr = s.accept()
    clients.append(sock_des)
    t = ReceiveThread(s, sock_des, clients)
    client_id += 1
    t.start()
    threads.append(t)

for t in threads:
    t.join()

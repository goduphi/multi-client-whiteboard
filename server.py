import socket
import threading


class ReceiveThread(threading.Thread):
    def __init__(self, sock, sock_desp, clients):
        threading.Thread.__init__(self)
        self.sock = sock
        self.sock_desp = sock_desp
        self.clients = clients
        self.message = None

    def run(self):
        print("Waiting to receive a message...")
        while True:
            self.receive_message()

    def receive_message(self):
        self.message = self.sock_desp.recv(1024)
        print(f"Received message: {self.message}")
        self.send_to_all_clients()

    def send_to_all_clients(self):
        for client in self.clients:
            client[0].send(self.message)


def notify_all_clients(addr, clients, client_id):
    for client in clients:
        if client_id != client[1]:
            message = "New client has joined the room: " + addr[0]
            client[0].send(bytes(message, 'utf-8'))


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
    print(f"New client joined: {addr}")
    clients.append((sock_des, client_id))
    notify_all_clients(addr, clients, client_id)
    client_id += 1
    t = ReceiveThread(s, sock_des, clients)
    t.start()
    threads.append(t)

for t in threads:
    t.join()

s.close()

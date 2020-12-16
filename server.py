import socket
import threading
import pickle


class ReceiveThread(threading.Thread):
    def __init__(self, sock, sock_desp, clients, client_id):
        threading.Thread.__init__(self)
        self.sock = sock
        self.sock_desp = sock_desp
        self.clients = clients
        self.message = None
        self.client_id = client_id

    def run(self):
        print("Waiting to receive a message...")
        while True:
            self.receive_message()

    def receive_message(self):
        self.message = pickle.loads(self.sock_desp.recv(2048))
        self.send_to_all_clients()

    def send_to_all_clients(self):
        for client in self.clients:
            try:
                client[0].send(pickle.dumps(self.message))
            except Exception as e:
                print(f"Send error: {e}")


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
    t = ReceiveThread(s, sock_des, clients, client_id)
    t.start()
    threads.append(t)
    client_id += 1

for t in threads:
    t.join()

s.close()

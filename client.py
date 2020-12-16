'''
The pygame code was directly copied from Geeksforgeeks
'''

import socket
import threading
import pickle
from utility import Vec2
import pygame
from pygame.locals import *
import sys

# Global position of a player
x = 200
y = 200


class ReceiveThread(threading.Thread):
    def __init__(self, sock, win):
        threading.Thread.__init__(self)
        self.sock = sock
        self.win = win

    def run(self):
        global x
        global y
        while True:
            position = pickle.loads(self.sock.recv(2048))
            x = position.x
            y = position.y
            pygame.draw.rect(self.win, (255, 0, 0), (x, y, 5, 5))


# Initialize all of the network code
# Note: All the static code will be changed later
s = socket.socket()
host = socket.gethostname()
port = 1100
s.connect((host, port))

# This is where the game code starts
pygame.init()
win = pygame.display.set_mode((800, 500))

# Instantiate and start the thread to receive data from all connected clients
user = ReceiveThread(s, win)
user.start()

# Helper to make sure I send data only when the object translates
updated = False
drawing = False

while True:
    pygame.time.delay(10)
    x, y = pygame.mouse.get_pos()
    # iterate over the list of Event objects
    # that was returned by pygame.event.get() method.
    for event in pygame.event.get():

        # if event object type is QUIT
        # then quitting the pygame
        # and program both.
        if event.type == pygame.QUIT:
            # it will make exit the while loop
            sys.exit()

        if event.type == MOUSEBUTTONDOWN:
            drawing = True
        elif event.type == MOUSEBUTTONUP:
            drawing = False

    if drawing:
        pygame.draw.rect(win, (255, 0, 0), (x, y, 5, 5))
        updated = True

    if updated:
        c = Vec2(x, y)
        s.send(pickle.dumps(c))
        updated = False

    # completely fill the surface object
    # with black colour
    # win.fill((0, 0, 0))
    # it refreshes the window
    pygame.display.update()

user.join()
s.close()
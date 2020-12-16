'''
The pygame code was directly copied from Geeksforgeeks
'''

import socket
import threading
import pickle
from utility import Vec2, Square
import pygame

# Global position of a player
x = 200
y = 200


class ReceiveThread(threading.Thread):
    def __init__(self, sock):
        threading.Thread.__init__(self)
        self.sock = sock

    def run(self):
        global x
        global y
        while True:
            position = pickle.loads(self.sock.recv(2048))
            x = position.x
            y = position.y


# Initialize all of the network code
# Note: All the static code will be changed later
s = socket.socket()
host = socket.gethostname()
port = 1100
s.connect((host, port))

# This is where the game code starts
pygame.init()
win = pygame.display.set_mode((500, 500))

# Instantiate and start the thread to receive data from all connected clients
user = ReceiveThread(s)
user.start()

# Helper to make sure I send data only when the object translates
updated = False

square = Square(50, 50)
vel = 10

while True:
    pygame.time.delay(10)

    # iterate over the list of Event objects
    # that was returned by pygame.event.get() method.
    for event in pygame.event.get():

        # if event object type is QUIT
        # then quitting the pygame
        # and program both.
        if event.type == pygame.QUIT:
            # it will make exit the while loop
            run = False
    # stores keys pressed
    keys = pygame.key.get_pressed()

    # if left arrow key is pressed
    if keys[pygame.K_LEFT] and x > 0:
        # decrement in x co-ordinate
        x -= vel
        updated = True

        # if left arrow key is pressed
    if keys[pygame.K_RIGHT] and x < 500 - square.x:
        # increment in x co-ordinate
        x += vel
        updated = True

        # if left arrow key is pressed
    if keys[pygame.K_UP] and y > 0:
        # decrement in y co-ordinate
        y -= vel
        updated = True

        # if left arrow key is pressed
    if keys[pygame.K_DOWN] and y < 500 - square.y:
        # increment in y co-ordinate
        y += vel
        updated = True

    if updated:
        c = Vec2(x, y)
        s.send(pickle.dumps(c))
        updated = False

    # completely fill the surface object
    # with black colour
    win.fill((0, 0, 0))

    # drawing object on screen which is rectangle here
    pygame.draw.rect(win, (255, 0, 0), (x, y, 50, 50))

    # it refreshes the window
    pygame.display.update()

user.join()
s.close()
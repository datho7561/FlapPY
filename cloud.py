# Import libraries
import random, pygame

# The cloud class
class Cloud:

    global SPEED

    def __init__(self, height, width):
        self.y = random.randint(0, height)
        self.x = width

    def move(self, speed):
        self.x += speed

    # TODO: implement a draw method for the cloud
    def getRect(self):
        return pygame.Rect(int(self.x), int(self.y), 1, 1)

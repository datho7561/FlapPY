import random, pygame

# Constants
WIDTH = 20

# The pipe class
class Pipe:

    global WIDTH

    def __init__(self, scrWidth, scrHeight):
        self.topPipe = random.randint(3*WIDTH, scrHeight - 6*WIDTH)
        self.bottomPipe = self.topPipe + int(4*WIDTH)
        self.x = scrWidth
        self.scoredOn = False
        self.screenHeight = scrHeight
        self.screenWidth = scrWidth

    def move(self, distance):
        self.x -= distance

    def getRect(self):
        return (pygame.Rect(self.x-WIDTH/2, 0, WIDTH, self.topPipe) , pygame.Rect(self.x-WIDTH/2, self.bottomPipe, WIDTH, self.screenHeight))

    def addScore(self):
        if ((not self.scoredOn) and (self.x < int(self.screenWidth/2))):
            self.scoredOn = True
            return 1
        return 0

    def checkCollision(self, other):
        return self.getRect()[0].colliderect(other) or self.getRect()[1].colliderect(other)

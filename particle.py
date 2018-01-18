# Import libraries
import random, math, pygame

# constants
PARTICLE_COLOURS = [ (255,0,0) , (255,255,0) , (255,128,0) ]

# The particle (subpart of the explosion) class
class Particle:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.v = random.random()*24-12
        self.direction = random.random()*2*math.pi
        self.vy = self.v * math.sin(self.direction)
        self.vx = self.v * math.cos(self.direction)
        self.colour = PARTICLE_COLOURS[random.randint(0,2)]
        self.lifetime = random.randint(20,60)

    def update(self):
        self.lifetime -= 1
        self.x += self.vx
        self.y += self.vy

    def getRect(self):
        return pygame.Rect(int(self.x), int(self.y), 2, 2)

    def getColour(self):
        return self.colour

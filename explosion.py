# Import libraries
import random
from particle import Particle

# The explosion class
class Explosion:

    def __init__(self, x, y):
        self.particles = list()
        self.numParticles = random.randint(100, 400)
        for i in range (self.numParticles):
            self.particles.append( Particle(x, y) )

    def update(self):
        for i in range(len(self.particles)):
            self.particles[i].update()
        self.particles = [particle for particle in self.particles if particle.lifetime > -1]

    def draw(self):
        rects = list()
        colours = list()
        for i in range(len(self.particles)):
            rects.append(self.particles[i].getRect())
            colours.append(self.particles[i].getColour())
        return rects, colours

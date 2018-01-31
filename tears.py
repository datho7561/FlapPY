import random
from pygame import Surface, draw

class Tears:

    global EVAPORATION_HEIGHT, COLOUR

    # Some variables
    EVAPORATION_HEIGHT = 50
    COLOUR = (51, 51, 255)

    def __init__(self, xPos, yPos, width, height):
        """ Make a new group of tears """
        self.x = xPos
        self.y = yPos
        self.tearList = []
        self.width = int(width)
        self.height = int(height)

    def update(self):
        """ Update the group of tears and return the image of them """
        for tear in self.tearList:
            tear.update()

        # Remove tears below cutoff range
        self.tearList = [tear for tear in self.tearList if not (tear.y - self.y) > EVAPORATION_HEIGHT]

        # Make a new image of tears
        image = Surface((self.width, self.height))
        image.fill((0, 0, 0))
        image.set_colorkey((0, 0, 0))

        # Draw each tear
        for tear in self.tearList:
            draw.rect(image, COLOUR, (tear.x, tear.y, 5, 5))

        # 50/50 chance to shed a new tear
        if (random.randint(0, 1)):
            self.tearList.append(Tear(self.x, self.y))

        # Return the image
        return image


class Tear:

    global BASE_SPEED

    BASE_SPEED = 2

    def __init__(self, xPos, yPos):
        self.x = xPos
        self.y = yPos - 5
        self.vy = 0
        self.v = BASE_SPEED if random.randint(0,1) else -BASE_SPEED
        if self.v < 0:
            self.x-=10

    def update(self):
        self.vy += .5 # Calculated from the bird acceleration of .5
        self.y += self.vy
        self.x += self.v

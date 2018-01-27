from pygame import Surface, draw

class Sky:

    global DAY1, DAY2, SET1, SET2, NIGHT1, NIGHT2, TRANSITION_FRAMES

    DAY1 = (102, 153, 255)
    DAY2 = (153, 204, 255)

    SET1 = (153, 0, 204)
    SET2 = (255, 51, 0)

    NIGHT1 = (0, 0, 0)
    NIGHT2 = (0, 0, 77)

    TRANSITION_FRAMES = 60

    def __init__(self, width, height):
        """ Create a new Sky object """
        self.image = Surface((width, height))
        self.transitionTimer = 0
        self.lastTime = 0

    def draw(self, time):
        """ Updates self based on time and draws self to screen,
        returning screen"""

        # If the transition is in effect, continue it
        if self.transitionTimer > 0:
            self.transitionTimer += 1
        # If the transition has gone through all the frames, end it
        if self.transitionTimer > TRANSITION_FRAMES:
            self.transitionTimer = 0
            self.lastTime = time
        # If the time has changed and the transition hasn't started yet, start it
        if self.lastTime != time and self.transitionTimer == 0:
            self.transitionTimer = 1

        # Print colour of gradient based on time of day,
        #  taking into account any transitions between times of day
        if self.lastTime == 0:
            self.gradient(self.transition(DAY1, SET1, self.transitionTimer),
                     self.transition(DAY2, SET2, self.transitionTimer))
        elif self.lastTime == 1:
            self.gradient(self.transition(SET1, NIGHT1, self.transitionTimer),
                     self.transition(SET2, NIGHT2, self.transitionTimer))
        else:
            self.gradient(self.transition(NIGHT1, DAY1, self.transitionTimer),
                     self.transition(NIGHT2, DAY2, self.transitionTimer))

        # Return the sky to be drawn
        return self.image

    def gradient(self, topColour, bottomColour):
        """ Draw a gradient based on the two given colours """
        colour = [topColour[0], topColour[1], topColour[2]]
        transition = [(bottomColour[0]-topColour[0])/self.image.get_height(),
                      (bottomColour[1]-topColour[1])/self.image.get_height(),
                      (bottomColour[2]-topColour[2])/self.image.get_height()]

        for i in range(self.image.get_height()):
            draw.line(self.image, (int(colour[0]), int(colour[1]), int(colour[2])),
                      (0, i), (self.image.get_width(), i))

            for j in range(3):
                colour[j] += transition[j]

    def transition(self, startColour, endColour, position):
        """ Linear interpolation between two colours based on transition time """
        return (startColour[0] + int(position * (endColour[0] - startColour[0]) / TRANSITION_FRAMES),
                startColour[1] + int(position * (endColour[1] - startColour[1]) / TRANSITION_FRAMES),
                startColour[2] + int(position * (endColour[2] - startColour[2]) / TRANSITION_FRAMES))

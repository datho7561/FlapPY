###############################################################################
# Author: David Thompson
# Created On: 17 January, 2017
# Purpose: A fun game about flapping a lot
###############################################################################



# Import important libraries. Note that pygame is used
import sys, os, pygame, random, math

# Declare window constants
size = width, height = 400, 300
dayColour = (128, 255, 255)
nightColour = (0, 0, 128)
pipeColour = (0, 255, 0)
pipeOutlineColour = (0, 102, 0)
titleColour = (153, 255, 51)
counterColour = (0, 0, 153)
gameoverColour = (230, 0, 0)
PARTICLE_COLOURS = [ (255,0,0) , (255,255,0) , (255,128,0) ]


### FUCNTIONS ###

def getResourcePath(name):
    """ Function to get a resource that's in the same folder as the script"""
    return (os.path.realpath(__file__)[0:len(os.path.realpath(__file__))-len(os.path.basename(__file__))] + name)


### CLASSES ###

# The pipe class
class Pipe:

    def __init__(self):
        self.topPipe = random.randint(3*birdHeight, height - 6*birdHeight)
        self.bottomPipe = self.topPipe + int(4*birdHeight)
        self.x = width
        self.scoredOn = False

    def move(self, distance):
        self.x -= distance

    def getRect(self):
        return (pygame.Rect(self.x-birdWidth/2, 0, birdWidth, self.topPipe) , pygame.Rect(self.x-birdWidth/2, self.bottomPipe, birdWidth, height))

    def addScore(self):
        if ((not self.scoredOn) and (self.x < int(width/2))):
            self.scoredOn = True
            return 1
        return 0

    def checkCollision(self, other):
        return self.getRect()[0].colliderect(other) or self.getRect()[1].colliderect(other)

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

# The cloud class
class Cloud:

    def __init__(self):
        self.y = random.randint(0, height)
        self.x = width
        self.vx = -birdVX/2

    def update(self):
        self.x += self.vx

    # TODO: implement a draw method for the cloud
    def getRect(self):
        return pygame.Rect(int(self.x), int(self.y), 1, 1)


### VARIABLE INITIALIZATION ###

# Initialize the bird variables
birdSize = birdWidth, birdHeight = 20, 20
birdY = height/2
birdVX = 2
birdVY = 0
birdAY = .5

# Pipe variables
pipes = list()
pipes.append(Pipe())
pipeTimer = 0

# Clouds variables
clouds = list()
clouds.append(Cloud())
cloudTimer = 40

# Sky variables
bgColour = dayColour

# Explosion variable
explosion = Explosion(0, 0)

# Game variables
score = 0
gameStarted = 0
noclip = False


# Initialize pygame
#  The method of initializing the sound engine first was taken directly from StackOverFlow:
#  https://stackoverflow.com/questions/18273722/pygame-sound-delay#18513365
pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.mixer.init()
pygame.init()
pygame.display.set_caption("Flappy")
screen = pygame.display.set_mode(size)

font = pygame.font.SysFont("Arial Bold", 72)
titleFont = pygame.font.SysFont("Bauhaus 93", 80)
gameoverFont = pygame.font.SysFont("Arial Bold", 48)

birdImg = pygame.image.load(getResourcePath("bird.png"))
birdImg.convert()
cloudImg = pygame.image.load(getResourcePath("cloud.png"))
cloudImg.convert()

flapSound = pygame.mixer.Sound(getResourcePath("flap.ogg"))


### GAME LOOP ###

while True:

    # amount of time to wait between frames
    pygame.time.Clock().tick(60)


    ### PROCESS EVENTS ###

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # If the close button is pressed, exit the program
            sys.exit()
        if event.type == pygame.KEYDOWN and event.key == 32:
            if gameStarted == 0:
                gameStarted = 1
                birdVY = -5
                flapSound.play()
            if gameStarted == 1:
                birdVY = -5
                flapSound.play()
        if event.type == pygame.KEYDOWN and event.key == 114:
            if gameStarted == 2:
                gameStarted = 0
                birdVY = 0
                birdY = height/2
                score = 0
                del pipes[:]
                pipes.append(Pipe())
                pipeTimer = 0
        if event.type == pygame.KEYDOWN and event.key == 113:
            noclip = True


    ### PROCESS GAME LOGIC ###

    # Update the bird
    if gameStarted == 1:

        # Move bird
        birdY += birdVY
        if birdY > height:
            # TODO: remove noclip
            if not noclip:
                birdY = height
                gameStarted = 2
                explosion = Explosion(int(width/2), birdY)
        if birdY < 0:
            birdY = 0
        birdVY += birdAY

    # Update the bird Rect as it is used for collision detection
    birdRect = pygame.Rect(int(width/2 - birdWidth/2), int(birdY - birdHeight/2), birdWidth, birdHeight)

    # Update the explosion progress
    explosion.update()

    # Update the pipes
    if gameStarted == 1:

        # Remove pipes that are out of bounds and add a new one if necessary
        pipes = [pipe for pipe in pipes if pipe.x > -birdWidth/2]
        pipeTimer += 1
        if pipeTimer >= 40:
            pipes.append(Pipe())
            pipeTimer = 0

        # Move pipes
        for i in range(len(pipes)):
            pipes[i].move(birdVX)
            score += pipes[i].addScore()
            if pipes[i].checkCollision(birdRect):
                # TODO: remove noclip
                if not noclip:
                    gameStarted = 2
                    explosion = Explosion(int(width/2), birdY)

    # update the clouds
    if gameStarted == 1:

        # Remove clouds that are out of bounds and add a new one if necessary
        clouds = [cloud for cloud in clouds if cloud.x > -birdWidth/2]
        cloudTimer -= 1
        if cloudTimer <= 0:
            clouds.append(Cloud())
            cloudTimer = random.randint(35,60)

        # Move clouds
        for i in range(len(clouds)):
            clouds[i].update()


    ### DRAW ###

    # Draw Sky

    # Update sky colour
    if score%20 < 10:
        if bgColour[2] < dayColour[2]:
            bgColour = (bgColour[0]+4, bgColour[1]+8, bgColour[2]+4)
        else:
            bgColour = dayColour
    else:
        if bgColour[2] > nightColour[2]:
            bgColour = (bgColour[0]-4, bgColour[1]-8, bgColour[2]-4)
        else:
            bgColour = nightColour

    try:
        screen.fill(bgColour)
    except:
        print(bgColour)


    for i in range(len(clouds)):
        screen.blit(cloudImg, clouds[i].getRect())

    # Draw bird
    screen.blit(birdImg, birdRect)

    # Draw pipes
    for i in range(len(pipes)):
        # Inside of rectangle
        pygame.draw.rect(screen, pipeColour, pipes[i].getRect()[0], 0)
        pygame.draw.rect(screen, pipeColour, pipes[i].getRect()[1], 0)
        # Border of rectangle
        pygame.draw.rect(screen, pipeOutlineColour, pipes[i].getRect()[0], 2)
        pygame.draw.rect(screen, pipeOutlineColour, pipes[i].getRect()[1], 2)

    # Draw the explosion
    if gameStarted == 2:
        explosionToDraw = explosion.draw()
        for i in range(len(explosionToDraw[0])):
            pygame.draw.rect(screen, explosionToDraw[1][i], explosionToDraw[0][i], 0)

    # Draw the title if the game hasn't started yet
    if gameStarted == 0:

        screen.blit(titleFont.render("Flappy", True, titleColour), pygame.Rect(int(width/2-titleFont.size("Flappy")[0]/2), 0, 1, 1))

    elif gameStarted == 1:

        # Translucent box behind score
        scoreScreen = pygame.Surface(font.size(str(score)))
        scoreScreen.set_alpha(192)
        scoreScreen.fill((0, 0, 0))
        screen.blit(scoreScreen, (0,0))

        # Score
        screen.blit(font.render(str(score), True, counterColour), (0,0))

    else:

        # This method of createing a translucent box came from StackOverFlow:
        #  https://stackoverflow.com/questions/6339057/draw-a-transparent-rectangle-in-pygame
        gameOverScreen = pygame.Surface((width, int(2*gameoverFont.size("l")[1])))
        gameOverScreen.set_alpha(192)
        gameOverScreen.fill((0, 0, 0))
        screen.blit(gameOverScreen, (0, int(height/2 - gameoverFont.size("l")[1])))

        # Game Over message with score over top of the translucent box
        fsString = "Final Score: " + str(score)
        resetString = "Press 'r' to reset"
        screen.blit(gameoverFont.render(fsString, True, gameoverColour), (int(width/2-gameoverFont.size(fsString)[0]/2), int(height/2 - gameoverFont.size("l")[1])))
        screen.blit(gameoverFont.render(resetString, True, gameoverColour), (int(width/2-gameoverFont.size(resetString)[0]/2), int(height/2)))

    pygame.display.flip()

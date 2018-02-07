###############################################################################
# Author: David Thompson
# Created On: 17 January, 2017
# Purpose: A fun game about flapping a lot
###############################################################################


# Import important libraries. Note that pygame is used
import sys, os, pygame, random, math

# Import self-created modules
from particle import Particle
from pipe import Pipe
from explosion import Explosion
from sky import Sky
from tears import Tears


### CONSTANTS ###

size = width, height = 800, 600
dayColour = (128, 255, 255)
sunsetColour = (255, 128, 0)
nightColour = (0, 0, 0)
pipeColour = (0, 255, 0)
pipeOutlineColour = (0, 102, 0)
counterColour = (200, 200, 200)
gameoverColour = (230, 0, 0)


### VARIABLE INITIALIZATION ###

# Initialize the bird variables
birdSize = birdWidth, birdHeight = 38, 38
birdY = height/2
birdVX = 2
birdVY = 0
birdAY = .5

# Pipe variables
pipes = list()
pipes.append(Pipe(width, height))
pipeTimer = 0

# Explosion variable
explosion = Explosion(0, 0)

# Tears variable
tears = Tears(0, 0, width, height)

# Game variables
score = 0
gameStarted = 0
noclip = False


### FUNCTIONS ###

def getResourcePath(name):
    """ Function to get a resource that's in the same folder as the script"""
    return (os.path.realpath(__file__)[0:len(os.path.realpath(__file__))-len(os.path.basename(__file__))] + name)

# Reset function
def reset():
    """ Resets the bird, pipes, sky, and game condition """
    # It is important that the game variables are global so that this function
    #  can reset them
    global score, gameStarted, bgColour, dayColour, pipes, birdVY, birdY, height
    global pipeTimer, theSky

    # Set everything back to its starting condition
    gameStarted = 0
    birdVY = 0
    birdY = height/2
    score = 0
    theSky.reset()
    del pipes[:]
    pipes.append(Pipe(width, height))
    pipeTimer = 0

# Reads the previous highscore and writes a new one if the current score is greater
def highscore():

    global score

    f = open(getResourcePath("highscore.txt"), "r")
    try:
        prevHighscore = int(f.read())
    except:
        prevHighscore = 0
    f.close()

    if (score > prevHighscore):
        f = open(getResourcePath("highscore.txt"), "w")
        f.write(str(score))
        f.close()
        return str(score)

    return str(prevHighscore)


### INITIALIZE PYGAME ###

# The method of initializing the sound engine first was taken directly from StackOverFlow:
#  https://stackoverflow.com/questions/18273722/pygame-sound-delay#18513365
#  This eliminates the lag otherwise prevalent in the sound engine
pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.mixer.init()
pygame.init()
pygame.display.set_caption("Flappy")
screen = pygame.display.set_mode(size)

# Initialize fonts
font = pygame.font.SysFont("Arial Bold", 72)
titleFont = pygame.font.SysFont("Bauhaus 93", 80)
gameoverFont = pygame.font.SysFont("Arial Bold", 48)

# Access images
birdImg = pygame.image.load(getResourcePath("bird.png"))
birdImg.convert()
cloudImg = pygame.image.load(getResourcePath("clouds.png"))
cloudImg.convert()
mountainImg = pygame.image.load(getResourcePath("mountains.png"))
mountainImg.convert()

# Load highscore
highscoreStr = highscore()

# Initialize the sky (doing this here because it needs the cloud and mountain img)
theSky = Sky(width, height, cloudImg, mountainImg)

# Access sounds and music
flapSound = pygame.mixer.Sound(getResourcePath("flap.ogg"))
music = pygame.mixer.Sound(getResourcePath("music.ogg"))
birdsSound = pygame.mixer.Sound(getResourcePath("birds.ogg"))
stopSound = pygame.mixer.Sound(getResourcePath("stop.ogg"))

# Start birds chirping
birdsSound.play(loops=-1)

### GAME LOOP ###

while True:

    # FRAMERATE
    pygame.time.Clock().tick(75)

    # For testing purposes
##    pygame.time.Clock().tick(150)


    ### PROCESS EVENTS ###

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # If the close button is pressed, exit the program
            sys.exit()
        if event.type == pygame.KEYDOWN and (event.key == 32):
            if gameStarted == 0:
                gameStarted = 1
                birdVY = -8
                birdsSound.stop()
                music.play(loops=-1)
                flapSound.play()
            if gameStarted == 1:
                birdVY = -8
                flapSound.play()
        if event.type == pygame.KEYDOWN and event.key == 114:
            if gameStarted == 2:
                reset()
                birdsSound.play(loops=-1)
        if event.type == pygame.KEYDOWN and event.key == 113:
            # TODO: remove implementation
            if noclip:
                noclip = False
            else:
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
                highscoreStr = highscore()
                music.stop()
                stopSound.play()

                # Create gameover effects (explosion and tears)
                explosion = Explosion(int(width/2), birdY)
                tears = Tears(int(width/2), birdY, width, height)
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
        if pipeTimer >= 80:
            pipes.append(Pipe(width, height))
            pipeTimer = 0

        # Move pipes
        for i in range(len(pipes)):
            pipes[i].move(birdVX)
            score += pipes[i].addScore()
            if pipes[i].checkCollision(birdRect):
                # TODO: remove noclip
                if not noclip:
                    gameStarted = 2
                    highscoreStr = highscore()
                    music.stop()
                    stopSound.play()
                    explosion = Explosion(int(width/2), birdY)
                    tears = Tears(int(width/2), birdY, width, height)

    ### DRAW ###

    # Draw sky
    screen.blit(theSky.draw(int(score%30//10)), (0, 0))

    # Draw bird
    screen.blit(birdImg, (birdRect[0]-1, birdRect[1]-1, birdRect[2], birdRect[3]))

    # Draw pipes
    for i in range(len(pipes)):
        # Inside of rectangle
        pygame.draw.rect(screen, pipeColour, pipes[i].getRect()[0], 0)
        pygame.draw.rect(screen, pipeColour, pipes[i].getRect()[1], 0)
        # Border of rectangle
        pygame.draw.rect(screen, pipeOutlineColour, pipes[i].getRect()[0], 2)
        pygame.draw.rect(screen, pipeOutlineColour, pipes[i].getRect()[1], 2)

    # Draw the explosion and tears
    if gameStarted == 2:
        # Tears
        screen.blit(tears.update(), (0,0,1,1))
        # Explosion
        explosionToDraw = explosion.draw()
        for i in range(len(explosionToDraw[0])):
            pygame.draw.rect(screen, explosionToDraw[1][i], explosionToDraw[0][i], 0)

    # Draw the title if the game hasn't started yet
    if gameStarted == 0:

        screen.blit(titleFont.render("Flappy", True, pipeColour), pygame.Rect(int(width/2-titleFont.size("Flappy")[0]/2), 0, 1, 1))

    elif gameStarted == 1:

        # Translucent box behind score
        scoreScreen = pygame.Surface(font.size(str(score)))
        scoreScreen.set_alpha(192)
        scoreScreen.fill((0, 0, 0))
        screen.blit(scoreScreen, (0,0))

        # Score
        screen.blit(font.render(str(score), True, counterColour), (0,0))

    else:

        # This method of creating a translucent box came from StackOverFlow:
        #  https://stackoverflow.com/questions/6339057/draw-a-transparent-rectangle-in-pygame
        gameOverScreen = pygame.Surface((width, int(2*gameoverFont.size("l")[1])))
        gameOverScreen.set_alpha(192)
        gameOverScreen.fill((0, 0, 0))
        screen.blit(gameOverScreen, (0, int(height/2 - gameoverFont.size("l")[1])))

        # Game Over message with score over top of the translucent box
        fsString = "Final Score: " + str(score) + "   Highscore: " + highscoreStr
        resetString = "Press 'r' to reset"
        screen.blit(gameoverFont.render(fsString, True, counterColour), (int(width/2-gameoverFont.size(fsString)[0]/2), int(height/2 - gameoverFont.size("l")[1])))
        screen.blit(gameoverFont.render(resetString, True, counterColour), (int(width/2-gameoverFont.size(resetString)[0]/2), int(height/2)))

    # For the built-in double buffer
    pygame.display.flip()

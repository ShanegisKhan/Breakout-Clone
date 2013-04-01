import pygame, sys, random
from pygame.locals import *

SCREEN_SIZE = 640, 480
FPS = 60
MOVESPEED = 5

# object dimension constants
PADDLE_WIDTH = 60
PADDLE_HEIGHT = 12
BRICK_WIDTH = 60
BRICK_HEIGHT = 15
BALL_DIAMETER = 16
BALL_RADIUS = BALL_DIAMETER / 2
BALL_SPEED = 5
ballDir = ''
lives = 3
bricks = []
score = 0


# Paddle y coordinates
PADDLE_Y = SCREEN_SIZE[1] - PADDLE_HEIGHT - 10

# Color constants
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BRICK_COLOR = (200, 200, 0)
PADDLE = pygame.Rect(300, PADDLE_Y, PADDLE_WIDTH, PADDLE_HEIGHT)
BALL = pygame.Rect(300, PADDLE_Y - BALL_DIAMETER, BALL_DIAMETER, BALL_DIAMETER)

# Generates a list of bricks
def getBricks():
    bricks = []
    y_ofs = 35
    for i in range(7):
        x_ofs = 35
        for j in range(8):
            bricks.append(pygame.Rect(x_ofs, y_ofs, BRICK_WIDTH, BRICK_HEIGHT))
            x_ofs += BRICK_WIDTH + 10
        y_ofs += BRICK_HEIGHT + 5
    return bricks

def drawBricks(score, ballDir):
    for brick in bricks[:]:
        pygame.draw.rect(windowSurface, BRICK_COLOR, (brick))
        
# Draws the list of bricks onto the screen                
def drawText(text, font, surface, x, y):
    textobj = font.render(text, 1, WHITE)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)
    
# Checks if the player has lost   
def gameOver():
    if lives == 0:
        pygame.mixer.music.stop()
        return True

# Terminates the program
def terminate():
    pygame.quit()
    sys.exit()

# waits for the correct key to be pressed to execute the terminate function    
def waitForKeyPress():
    for event in pygame.event.get():
        if event.type == QUIT:
            terminate()
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                terminate()

# Checks to see if the player has won/                
def gameWon():
    if len(bricks) == 0:
        return True
    
def playMusic():
    musicChoice = random.randint(0, 1)
    if musicChoice == 0:
        pygame.mixer.music.load('tetrisb.mid')
    else:
        pygame.mixer.music.load('tetrisc.mid')
    pygame.mixer.music.play(-1, 0.0)

# Set up for the game and screen.
pygame.init()
windowSurface = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption('Breakout!')
pygame.mouse.set_visible(False)
mainClock = pygame.time.Clock()
moveLeft = moveRight = False
ballUpLeft = ballDownLeft = ballUpRight = ballDownRight = False
playing = 'no'
bricks = getBricks()

# sets up sounds
playMusic()
bounceSound = pygame.mixer.Sound('bounce.wav')
breakBrick = pygame.mixer.Sound('pickup.wav')

# Starting the game loop
while True:
    windowSurface.fill(BLUE)
    pygame.draw.rect(windowSurface, RED, PADDLE)
    drawBricks(score, ballDir)
    
  
    for event in pygame.event.get():
        # Assigning controls for the game.
        if event.type == KEYDOWN:
            if event.key == K_LEFT or event.key == ord('a'):
                moveRight = False
                moveLeft = True
            if event.key == K_RIGHT or event.key == ord('d'):
                moveLeft = False
                moveRight = True
            if event.key == K_SPACE and playing == 'no' and not gameWon():
                playing = 'yes'
                ballDir = 'upRight'
            #elif event.key == K_SPACE and playing == 'yes' and lives > 0 and not gameWon():
                #playing = 'restart'
            elif event.key == K_SPACE and playing == 'restart' and lives > 0 and not gameWon():
                playing = 'yes'
                ballDir = 'upRight'
            if event.key == K_RETURN and gameOver() or gameWon():
                lives = 3
                score = 0 
                bricks = getBricks()
                playing = 'restart'
                playMusic()
                
                
        if event.type == KEYUP:
            if event.key == K_ESCAPE:
                terminate()
            if event.key == K_LEFT or event.key == ord('a'):
                moveLeft = False
            if event.key == K_RIGHT or event.key == ord('d'):
                moveRight = False
                
        if event.type == MOUSEMOTION:
                # If the mouse moves, move the player where the cursor is.
                PADDLE.move_ip(event.pos[0] - PADDLE.centerx, 0)
        
        # returns ball to paddle.        
        if playing == 'no':
            BALL.left = PADDLE.left + PADDLE.width / 2
            BALL.top = PADDLE.top - BALL.height
            ballDir = ''
                
    if moveLeft and PADDLE.left > 0:
        PADDLE.move_ip(-1 * MOVESPEED, 0)
    if moveRight and PADDLE.right < SCREEN_SIZE[0]:
        PADDLE.move_ip(MOVESPEED, 0)    
    
    # Ball and border collision detection
    if BALL.left < 0:
        if ballDir == 'upLeft':
            ballDir = 'upRight'
        if ballDir == 'downLeft':            
            ballDir = 'downRight'
    if BALL.right > SCREEN_SIZE[0]:
        if ballDir == 'upRight':
            ballDir = 'upLeft'
        if ballDir == 'downRight':
            ballDir = 'downLeft'
    if BALL.top < 0:
        if ballDir == 'upLeft':
            ballDir = 'downLeft'
        if ballDir == 'upRight':
            ballDir = 'downRight'
    if BALL.bottom > SCREEN_SIZE[1]:
        BALL = pygame.Rect(300, PADDLE_Y - BALL_DIAMETER, BALL_DIAMETER, BALL_DIAMETER)
        lives = lives - 1
        ballDir = ''
        playing = 'restart'
    
    # plays bounce sound effect if ball collides with sides or paddle    
    if BALL.left < 0 or BALL.right > SCREEN_SIZE[0] or BALL.top < 0 or BALL.colliderect(PADDLE):
        breakBrick.play()
    
    # Ball and paddle collision detection    
    if BALL.colliderect(PADDLE):
        BALL.top = PADDLE_Y - BALL_DIAMETER
        if ballDir == 'downLeft':
            ballDir = 'upLeft'
        if ballDir == 'downRight':
            ballDir = 'upRight'

# Ball and brick collision detection
    for brick in bricks[:]:
        if BALL.colliderect(brick):
            breakBrick.play()
            score += 3
            if ballDir == 'upLeft':
                ballDir = 'downLeft'
            elif ballDir == 'downLeft':            
                ballDir = 'upLeft'
            elif ballDir == 'upRight':
                ballDir = 'downRight'
            elif ballDir == 'downRight':
                ballDir = 'upRight'
            bricks.remove(brick)

    # move the ball for each of the four directions
    if ballDir == 'upLeft':
        BALL.left -= BALL_SPEED
        BALL.top -= BALL_SPEED
    if ballDir == 'upRight':
        BALL.left += BALL_SPEED
        BALL.top -= BALL_SPEED
    if ballDir == 'downLeft':
        BALL.left -= BALL_SPEED
        BALL.top += BALL_SPEED
    if ballDir == 'downRight':
        BALL.left += BALL_SPEED
        BALL.top += BALL_SPEED
   
    
    # Returns ball to starting position. 
    elif playing == 'restart':
        BALL = pygame.Rect(300, PADDLE_Y - BALL_DIAMETER, BALL_DIAMETER, BALL_DIAMETER)
        BALL.left = PADDLE.left + PADDLE.width / 2
        BALL.top = PADDLE.top - BALL.height 
        
    # set the mouse position to the center of the paddle
    pygame.mouse.set_pos(PADDLE.centerx, PADDLE.centery)
    # Draw the ball
    pygame.draw.circle(windowSurface, GREEN, (BALL.left, BALL.top), 8, 0)
    
    font = pygame.font.SysFont(None, 48)
    drawText('Score: %s Lives: %s' % (score, lives), font, windowSurface, 205, 5)
    
        
    # Check if the player has lost    
    if gameOver():
        drawText('Game over!', font, windowSurface, (SCREEN_SIZE[0] / 3), (SCREEN_SIZE[1] / 2))
    # Check to see if the player has won
    if gameWon():
        drawText('A winner is you :D', font, windowSurface, (SCREEN_SIZE[0] / 3), (SCREEN_SIZE[1] / 2))
        playing = 'no'           
    pygame.display.update()
    waitForKeyPress()
    mainClock.tick(FPS)
    
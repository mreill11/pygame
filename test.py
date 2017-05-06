# Paradigms Final Project: Multiplayer Pong Game
# Authors: Matt Reilly & Nick Palutsis
# Date: May 10, 2017

import random
import pygame, sys
from pygame.locals import *

#globals
screenWidth = 700
screenHeight = 500
paddleWidth = 24
paddleHeight = 80
ballRadius = 10
positionPlayer1 = 0
positionPlayer2 = 0
positionBall = [0, 0]
velocityPlayer1 = 0
velocityPlayer2 = 0
velocityBall = [0, 0]
scorePlayer1 = 0
scorePlayer2 = 0
borderThickness = 4

#colors
whiteColor = (255, 255, 255)
redColor = (255, 0, 0)
greenColor = (0, 255, 0)
blackColor = (0, 0, 0)
navyColor = (17, 36, 76)
goldColor = (194, 152, 50)

class GameSpace:
    def main(self):
        global positionPlayer1, velocityPlayer1, scorePlayer1, positionPlayer2, velocityPlayer2, scorePlayer2
        pygame.init()
        fps = pygame.time.Clock()

        #canvas declaration
        window = pygame.display.set_mode((screenWidth, screenHeight), 0, 32)
        pygame.display.set_caption("Let's Play Pong!") 

        self.background = pygame.Surface(window.get_size())
        self.background = self.background.convert()
        self.background.fill((blackColor))

        self.field = Gameboard(self)
        self.sprites = pygame.sprite.Group()
        self.board = pygame.sprite.RenderPlain(self.field)
        self.sprites.add(self.board)

        positionPlayer1 = [(paddleWidth / 2) - 1, screenHeight / 2]
        positionPlayer2 = [screenWidth + 1 - (paddleWidth / 2), screenHeight / 2]
        scorePlayer1 = 0
        scorePlayer2 = -1

        window.blit(self.background, (0,0))
        pygame.display.flip()


        #game loop
        while True:

            for event in pygame.event.get():

                if event.type == KEYDOWN:
                    keydown(event)
                elif event.type == KEYUP:
                    keyup(event)
                elif event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                    
            # pygame.display.update()
            fps.tick(60)

            window.fill(blackColor)
            self.sprites.update()
            self.sprites.draw(window)
            draw(window)
            pygame.display.flip()

# helper function that spawns a ball, returns a position vector and a velocity vector
# if right is True, spawn to the right, else spawn to the left
def ball_init(right):
    global positionBall, velocityBall # these are vectors stored as lists
    positionBall = [screenWidth / 2, screenHeight / 2]
    horz = random.randrange(1, 5)
    vert = random.randrange(1, 3)
    
    if right == False:
        horz = - horz

    velocityBall = [horz, -vert]

# # define event handlers
# def init():
#     global positionPlayer1, positionPlayer2, velocityPlayer1, velocityPlayer2, scorePlayer1, scorePlayer2  # these are floats
#     # global score1, score2  # these are ints
#     positionPlayer1 = [(paddleWidth / 2) - 1, screenHeight / 2]
#     positionPlayer2 = [screenWidth + 1 - (paddleWidth / 2), screenHeight / 2]
#     scorePlayer1 = 0
#     scorePlayer2 = 0

#     if random.randrange(0, 2) == 0:
#         ball_init(True)
#     else:
#         ball_init(False)

#     # self.field = self.Gameboard(self)
#     # self.gameboard = pygame.sprite.RenderPlain(self.field)


#draw function of canvas
def draw(canvas):
    global positionPlayer1, positionPlayer2, positionBall, velocityBall, scorePlayer1, scorePlayer2
           
    # canvas.fill(blackColor)

    # Draw the playing field
    # pygame.draw.line(canvas,
    #     whiteColor, 
    #     [screenWidth / 2, 0],
    #     [screenWidth / 2, screenHeight], 
    #     8)

    # pygame.draw.line(canvas, 
    #     whiteColor, 
    #     [paddleWidth + 1, 0],
    #     [paddleWidth + 1, screenHeight], 
    #     8)

    # pygame.draw.line(canvas, 
    #     whiteColor, 
    #     [screenWidth - paddleWidth - 2, 0],
    #     [screenWidth - paddleWidth - 2, screenHeight], 
    #     8)

    # pygame.draw.circle(canvas, 
    #     whiteColor, 
    #     [screenWidth // 2, screenHeight // 2], 
    #     50, 
    #     8)

    # update paddle's vertical position, keep paddle on the screen
    if positionPlayer1[1] > (paddleHeight / 2) and positionPlayer1[1] < screenHeight - (paddleHeight / 2):
        positionPlayer1[1] += velocityPlayer1
    elif positionPlayer1[1] == (paddleHeight / 2) and velocityPlayer1 > 0:
        positionPlayer1[1] += velocityPlayer1
    elif positionPlayer1[1] == screenHeight - (paddleHeight / 2) and velocityPlayer1 < 0:
        positionPlayer1[1] += velocityPlayer1
    
    if positionPlayer2[1] > (paddleHeight / 2) and positionPlayer2[1] < screenHeight - (paddleHeight / 2):
        positionPlayer2[1] += velocityPlayer2
    elif positionPlayer2[1] == (paddleHeight / 2) and velocityPlayer2 > 0:
        positionPlayer2[1] += velocityPlayer2
    elif positionPlayer2[1] == screenHeight - (paddleHeight / 2) and velocityPlayer2 < 0:
        positionPlayer2[1] += velocityPlayer2

    #update ball
    positionBall[0] += int(velocityBall[0])
    positionBall[1] += int(velocityBall[1])

    #draw paddles and ball
    pygame.draw.circle(canvas, 
        redColor, 
        positionBall, 
        ballRadius, 
        0)

    pygame.draw.circle(canvas, 
        whiteColor, 
        positionBall, 
        ballRadius + borderThickness, 
        borderThickness)

    pygame.draw.polygon(canvas, 
        goldColor, 
        [[positionPlayer1[0] - (paddleWidth / 2), positionPlayer1[1] - (paddleHeight / 2)], 
        [positionPlayer1[0] - (paddleWidth / 2), positionPlayer1[1] + (paddleHeight / 2)], 
        [positionPlayer1[0] + (paddleWidth / 2), positionPlayer1[1] + (paddleHeight / 2)], 
        [positionPlayer1[0] + (paddleWidth / 2), positionPlayer1[1] - (paddleHeight / 2)]], 
        0)

    pygame.draw.polygon(canvas, 
        goldColor, 
        [[positionPlayer2[0] - (paddleWidth / 2), positionPlayer2[1] - (paddleHeight / 2)], 
        [positionPlayer2[0] - (paddleWidth / 2), positionPlayer2[1] + (paddleHeight / 2)], 
        [positionPlayer2[0] + (paddleWidth / 2), positionPlayer2[1] + (paddleHeight / 2)], 
        [positionPlayer2[0] + (paddleWidth / 2), positionPlayer2[1] - (paddleHeight / 2)]], 
        0)

    pygame.draw.polygon(canvas, 
        navyColor, 
        [[positionPlayer1[0] - (paddleWidth / 2) + borderThickness/2, positionPlayer1[1] - (paddleHeight / 2)], 
        [positionPlayer1[0] - (paddleWidth / 2) + borderThickness/2, positionPlayer1[1] + (paddleHeight / 2)], 
        [positionPlayer1[0] + (paddleWidth / 2), positionPlayer1[1] + (paddleHeight / 2)], 
        [positionPlayer1[0] + (paddleWidth / 2), positionPlayer1[1] - (paddleHeight / 2)]], 
        borderThickness)

    pygame.draw.polygon(canvas, 
        navyColor, 
        [[positionPlayer2[0] - (paddleWidth / 2), positionPlayer2[1] - (paddleHeight / 2)], 
        [positionPlayer2[0] - (paddleWidth / 2), positionPlayer2[1] + (paddleHeight / 2)], 
        [positionPlayer2[0] + (paddleWidth / 2) - borderThickness, positionPlayer2[1] + (paddleHeight / 2)], 
        [positionPlayer2[0] + (paddleWidth / 2) - borderThickness, positionPlayer2[1] - (paddleHeight / 2)]], 
        borderThickness)

    #ball collision check on top and bottom walls
    if int(positionBall[1]) <= ballRadius:
        velocityBall[1] = - velocityBall[1]
    if int(positionBall[1]) >= screenHeight + 1 - ballRadius:
        velocityBall[1] = -velocityBall[1]
    
    #ball collison check on gutters or paddles
    if int(positionBall[0]) <= ballRadius + paddleWidth and int(positionBall[1]) in range(positionPlayer1[1] - (paddleHeight / 2),positionPlayer1[1] + (paddleHeight / 2), 1):
        velocityBall[0] = -velocityBall[0]
        velocityBall[0] *= 1.1
        velocityBall[1] *= 1.1
    elif int(positionBall[0]) <= ballRadius + paddleWidth:
        scorePlayer2 += 1
        ball_init(True)
        
    if int(positionBall[0]) >= screenWidth + 1 - ballRadius - paddleWidth and int(positionBall[1]) in range(positionPlayer2[1] - (paddleHeight / 2),positionPlayer2[1] + (paddleHeight / 2),1):
        velocityBall[0] = -velocityBall[0]
        velocityBall[0] *= 1.1
        velocityBall[1] *= 1.1
    elif int(positionBall[0]) >= screenWidth + 1 - ballRadius - paddleWidth:
        scorePlayer1 += 1
        ball_init(False)

    #update scores
    font1 = pygame.font.SysFont("Arial", 20)
    label1 = font1.render("Score " + str(scorePlayer1), 1, whiteColor)
    canvas.blit(label1, (50, 20))

    font2 = pygame.font.SysFont("Arial", 20)
    label2 = font2.render("Score " + str(scorePlayer2), 1, whiteColor)
    canvas.blit(label2, (550, 20))    
    
#keydown handler
def keydown(event):
    global velocityPlayer1, velocityPlayer2
    
    if event.key == K_UP:
        velocityPlayer2 = -8
    elif event.key == K_DOWN:
        velocityPlayer2 = 8
    elif event.key == K_w:
        velocityPlayer1 = -8
    elif event.key == K_s:
        velocityPlayer1 = 8

#keyup handler
def keyup(event):
    global velocityPlayer1, velocityPlayer2
    
    if event.key in (K_w, K_s):
        velocityPlayer1 = 0
    elif event.key in (K_UP, K_DOWN):
        velocityPlayer2 = 0

class Gameboard(pygame.sprite.Sprite):
    def __init__(self, environment):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = loadImage("./football_field.jpg")
        self.image = pygame.transform.scale(self.image, (screenWidth, screenHeight))
        self.rect.topleft = (0, 0)

    def update(self):
        self.rect.x = self.rect.x
        self.rect.y = self.rect.y    

def loadImage(name, colorkey = None):
    try:
        image = pygame.image.load(name)
    except pygame.error:
        print ("Failed to load image: ", fullname)
        raise SystemExit(str(geterror()))

    if image.get_alpha is None:
        image = image.convert()
    else:
        image = image.convert_alpha()

    return image, image.get_rect()

def loadImageOnly(name):
    try:
        image = pygame.image.load(name)
    except pygame.error:
        print ("Failed to load images: ", fullname)
        raise SystemExit(str(geterror()))

    if image.get_alpha is None:
        image = image.convert()
    else:
        image = image.convert_alpha()

    return image

#####################################################################  
############################ Play Game ##############################
#####################################################################   

if __name__ == "__main__":
    gs = GameSpace()
    gs.main()

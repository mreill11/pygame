# Paradigms Final Project: Multiplayer Pong Game
# Authors: Matt Reilly & Nick Palutsis
# Date: May 10, 2017

import random
import pygame, sys
from pygame.locals import *

# Global variables
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
play = False

# Colors
whiteColor = (255, 255, 255)
blackColor = (0, 0, 0)
redColor = (255, 0, 0)
navyColor = (17, 36, 76)
goldColor = (194, 152, 50)

class GameSpace:
    def main(self):
        global positionPlayer1, velocityPlayer1, scorePlayer1, positionPlayer2, velocityPlayer2, scorePlayer2
        self.isPlayer1 = False
        # if playerNum == 1:
        #     self.isPlayer1 = True
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
        scorePlayer2 = 0
        ball_init(True)

        window.blit(self.background, (0,0))
        pygame.display.flip()

        fps.tick(60)
        window.fill(blackColor)
        self.sprites.update()
        self.sprites.draw(window)
        draw(window)
        pygame.display.flip()

        # Loop to play the game
        while True:

            for event in pygame.event.get():

                if event.type == KEYDOWN:
                    keydown(event)
                    # self.sendData("DOWN")
                elif event.type == KEYUP:
                    keyup(event)
                    # self.sendData("UP")
                elif event.type == QUIT:
                    # reactor.stop()
                    pygame.quit()
                    sys.exit()

            if play:    # Wait until user presses spacebar to start
                fps.tick(60)

                window.fill(blackColor)
                # self.sprites.update()
                self.sprites.draw(window)
                draw(window)
                pygame.display.flip()
            else:       # Display pause screen
                window.fill(blackColor)
                # self.sprites.update()
                self.sprites.draw(window)

                font3Background = pygame.font.SysFont("Arial", 48, bold = True)
                pausedBackground = font3Background.render("Press Space to Play", 1, blackColor)
                window.blit(pausedBackground, (120, 225))  

                font3Foreground = pygame.font.SysFont("Arial", 48 , bold = True)
                pausedForeground = font3Foreground.render("Press Space to Play", 1, whiteColor)
                window.blit(pausedForeground, (125, 220))  

                pygame.display.flip()

    # def sendData(self, eventKey):
    #     if self.isPlayer1:
    #         self.outgoingConn.transport.write("1:" + eventKey)
    #     else:
    #         self.outgoingConn.transport.write("2:" + eventKey)

    # def transferConnectionObject(self, obj):
    #     self.outgoingConn = obj

    # def handleData(self, data):
    #     positionPlayer1 = int(data['posPlayer1'])
    #     positionPlayer2 = int(data['posPlayer2'])
    #     positionBall = int(data['posBall'])
    #     velocityPlayer1 = int(data['velPlayer1'])
    #     velocityPlayer1 = int(data['velPlayer2'])
    #     velocityBall = int(data['velBall'])
    #     scorePlayer1 = int(data['scorePlayer1'])
    #     scorePlayer2 = int(data['scorePlayer2'])

def ball_init(right):
    global positionBall, velocityBall
    positionBall = [screenWidth / 2, screenHeight / 2]
    horz = random.randrange(5, 10)
    vert = random.randrange(3, 7)
    
    if right == False:
        horz = - horz

    velocityBall = [horz, -vert]

# Draw the shapes (paddles, ball, etc.)
def draw(canvas):
    global positionPlayer1, positionPlayer2, positionBall, velocityBall, scorePlayer1, scorePlayer2, play

    # Move the paddles if they are within the bounds of the screen
    # Left paddle
    if positionPlayer1[1] > (paddleHeight / 2) + borderThickness and positionPlayer1[1] < screenHeight - (paddleHeight / 2) - borderThickness:      # paddle is between top and bottom
        positionPlayer1[1] += velocityPlayer1
    elif positionPlayer1[1] <= (paddleHeight / 2) + borderThickness and velocityPlayer1 > 0:      # paddle is at top & moving down
        positionPlayer1[1] += velocityPlayer1
    elif positionPlayer1[1] >= screenHeight - (paddleHeight / 2) - borderThickness and velocityPlayer1 < 0:       # paddle is at bottom & moving up
        positionPlayer1[1] += velocityPlayer1

    # Right paddle
    if positionPlayer2[1] > (paddleHeight / 2) + borderThickness and positionPlayer2[1] < screenHeight - (paddleHeight / 2) - borderThickness:      # paddle is between top and bottom
        positionPlayer2[1] += velocityPlayer2
    elif positionPlayer2[1] <= (paddleHeight / 2) + borderThickness and velocityPlayer2 > 0:      # paddle is at top & moving down
        positionPlayer2[1] += velocityPlayer2
    elif positionPlayer2[1] >= screenHeight - (paddleHeight / 2) - borderThickness and velocityPlayer2 < 0:       # paddle is at bottom & moving up
        positionPlayer2[1] += velocityPlayer2

    # Update the ball's position
    positionBall[0] += int(velocityBall[0])
    positionBall[1] += int(velocityBall[1])

    # Draw ball
    pygame.draw.circle(canvas, 
        redColor, 
        positionBall, 
        ballRadius, 
        0)

    # Draw ball border
    pygame.draw.circle(canvas, 
        whiteColor, 
        positionBall, 
        ballRadius + borderThickness, 
        borderThickness)

    # Draw left paddle
    pygame.draw.polygon(canvas, 
        goldColor, 
        [[positionPlayer1[0] - (paddleWidth / 2), positionPlayer1[1] - (paddleHeight / 2)], 
        [positionPlayer1[0] - (paddleWidth / 2), positionPlayer1[1] + (paddleHeight / 2)], 
        [positionPlayer1[0] + (paddleWidth / 2), positionPlayer1[1] + (paddleHeight / 2)], 
        [positionPlayer1[0] + (paddleWidth / 2), positionPlayer1[1] - (paddleHeight / 2)]], 
        0)

    # Draw left paddle border
    pygame.draw.polygon(canvas, 
        navyColor, 
        [[positionPlayer1[0] - (paddleWidth / 2) + borderThickness/2, positionPlayer1[1] - (paddleHeight / 2)], 
        [positionPlayer1[0] - (paddleWidth / 2) + borderThickness/2, positionPlayer1[1] + (paddleHeight / 2)], 
        [positionPlayer1[0] + (paddleWidth / 2), positionPlayer1[1] + (paddleHeight / 2)], 
        [positionPlayer1[0] + (paddleWidth / 2), positionPlayer1[1] - (paddleHeight / 2)]], 
        borderThickness)

    # Draw right paddle
    pygame.draw.polygon(canvas, 
        goldColor, 
        [[positionPlayer2[0] - (paddleWidth / 2), positionPlayer2[1] - (paddleHeight / 2)], 
        [positionPlayer2[0] - (paddleWidth / 2), positionPlayer2[1] + (paddleHeight / 2)], 
        [positionPlayer2[0] + (paddleWidth / 2), positionPlayer2[1] + (paddleHeight / 2)], 
        [positionPlayer2[0] + (paddleWidth / 2), positionPlayer2[1] - (paddleHeight / 2)]], 
        0)

    # Draw right paddle border
    pygame.draw.polygon(canvas, 
        navyColor, 
        [[positionPlayer2[0] - (paddleWidth / 2), positionPlayer2[1] - (paddleHeight / 2)], 
        [positionPlayer2[0] - (paddleWidth / 2), positionPlayer2[1] + (paddleHeight / 2)], 
        [positionPlayer2[0] + (paddleWidth / 2) - borderThickness, positionPlayer2[1] + (paddleHeight / 2)], 
        [positionPlayer2[0] + (paddleWidth / 2) - borderThickness, positionPlayer2[1] - (paddleHeight / 2)]], 
        borderThickness)
    
    # Check if ball hit left paddle; reverse x direction and increase ball speed
    if int(positionBall[0]) <= ballRadius + paddleWidth and int(positionBall[1]) in range(positionPlayer1[1] - (paddleHeight / 2) - (borderThickness * 4), positionPlayer1[1] + (paddleHeight / 2) + (borderThickness * 4), 1):
        velocityBall[0] = -velocityBall[0]
        velocityBall[0] *= 1.1
        velocityBall[1] *= 1.1
    # Ball missed left paddle; increase player 2 score and reset
    elif int(positionBall[0]) <= ballRadius + paddleWidth:
        scorePlayer2 += 1
        ball_init(True)
    
    # Check if ball hit right paddle; reverse x direction and increase ball speed
    if int(positionBall[0]) >= screenWidth + 1 - ballRadius - paddleWidth and int(positionBall[1]) in range(positionPlayer2[1] - (paddleHeight / 2) - (borderThickness * 4), positionPlayer2[1] + (paddleHeight / 2) + (borderThickness * 4), 1):
        velocityBall[0] = -velocityBall[0]
        velocityBall[0] *= 1.1
        velocityBall[1] *= 1.1
    # Ball missed right paddle; increase player 1 score and reset
    elif int(positionBall[0]) >= screenWidth + 1 - ballRadius - paddleWidth:
        scorePlayer1 += 1
        ball_init(False)

    # Check if ball hit top or bottom wall
    if int(positionBall[1]) <= ballRadius:
        velocityBall[1] = - velocityBall[1]
    if int(positionBall[1]) >= screenHeight + 1 - ballRadius:
        velocityBall[1] = -velocityBall[1]

    # Display scores
    font1Background = pygame.font.SysFont("Arial", 20, bold = True)
    homeBackground = font1Background.render("Home: " + str(scorePlayer1), 1, blackColor)
    canvas.blit(homeBackground, (63, 22))

    font1Foreground = pygame.font.SysFont("Arial", 20, bold = True)
    homeForeground = font1Foreground.render("Home: " + str(scorePlayer1), 1, whiteColor)
    canvas.blit(homeForeground, (65, 20))

    font2Background = pygame.font.SysFont("Arial", 20, bold = True)
    awayBackground = font2Background.render("Away: " + str(scorePlayer2), 1, blackColor)
    canvas.blit(awayBackground, (563, 22))  

    font2Foreground = pygame.font.SysFont("Arial", 20, bold = True)
    awayForeground = font2Foreground.render("Away: " + str(scorePlayer2), 1, whiteColor)
    canvas.blit(awayForeground, (565, 20))   
    
# User pressed key down
def keydown(event):
    global velocityPlayer1, velocityPlayer2, play
    
    if event.key == K_SPACE:
        if play:
            play = False
        else:
            play = True
    elif event.key == K_UP:
        velocityPlayer2 = -16
    elif event.key == K_DOWN:
        velocityPlayer2 = 16
    elif event.key == K_w:
        velocityPlayer1 = -16
    elif event.key == K_s:
        velocityPlayer1 = 16

# User released key
def keyup(event):
    global velocityPlayer1, velocityPlayer2
    
    if event.key in (K_w, K_s):
        velocityPlayer1 = 0
    elif event.key in (K_UP, K_DOWN):
        velocityPlayer2 = 0

# Setup field
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

#####################################################################  
############################ Play Game ##############################
#####################################################################   

if __name__ == "__main__":
    gs = GameSpace()
    gs.main()

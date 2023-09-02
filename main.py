from email import message
import random  # for generating random numbers
import sys  # for exit function to exit the program
import pygame
from pygame.locals import *
import time

#global variables
FPS = 32
SCREENWIDTH = 289
SCREENHEIGHT = 511
SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
GROUNDY = SCREENHEIGHT*0.8
GAME_SPRITES = {}
GAME_SOUNDS = {}
PLAYER = "gallery/sprites/bird.png"
BACKGROUND = 'gallery/sprites/background.jpg'
PIPE = 'gallery/sprites/pipe.jpg'


def welcomeScreen():
    '''
    shows image in the background
    '''
    playy = int(SCREENWIDTH/1.1)
    playx = int((SCREENWIDTH-GAME_SPRITES['play'].get_width())/2)
    messagex = int((SCREENWIDTH-GAME_SPRITES['message'].get_width())/2)
    messagey = int(SCREENHEIGHT*0.13)
    basex = 0
    while True:
        for event in pygame.event.get():
            # if user clicks on close button, close the game
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            # if user clicks on start button,start the game
            elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                return

            else:
                SCREEN.blit(GAME_SPRITES['background'], (0, 0))
                SCREEN.blit(GAME_SPRITES['play'], (playx, playy))
                SCREEN.blit(GAME_SPRITES['message'], (messagex, messagey))
                SCREEN.blit(GAME_SPRITES['base'], (basex, GROUNDY))
                pygame.display.update()
                FPSCLOCK.tick(FPS)


def maingame():
    score = 0
    playerx = int(SCREENWIDTH/5)
    playery = int((SCREENHEIGHT-GAME_SPRITES['player'].get_height())/2)
    basex = 0

    # creating two pipes for blitting in the screen
    newPipe1 = getRandomPipe()
    newPipe2 = getRandomPipe()

    # upper pipes
    upperPipes = [
        {'x': SCREENWIDTH+200, 'y': newPipe1[0]['y']},
        {'x': SCREENWIDTH+200+(SCREENWIDTH/2), 'y': newPipe2[0]['y']},
    ]
    # lower pipes
    lowerPipes = [
        {'x': SCREENWIDTH+200, 'y': newPipe1[1]['y']},
        {'x': SCREENWIDTH+200+(SCREENWIDTH/2), 'y': newPipe2[1]['y']},
    ]

    pipeVelx = -4
    playerVelY = -9
    playerMaxVelY = 10
    playerMinVelY = -8
    playerAccY = 1

    playerFlapAccv = -8  # velocity while flapping
    playerFlapped = False  # It is true only when the bird is flapping

    while True:
        for event in pygame.event.get():
            # if user clicks on close button, close the game
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            # if user clicks on start button,start the game
            elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if playery > 0:
                    playerVelY = playerFlapAccv
                    playerFlapped = True
                    # GAME_SOUNDS['wing'].play()

        # return true if bird collide with pipe that means player is crash
        crash = isCollide(playerx, playery, upperPipes, lowerPipes)
        if crash == True:
            return
        # calculating score
        playerMidPos = playerx+(GAME_SPRITES['player'].get_width()/2)
        for pipe in upperPipes:
            pipeMidPos = pipe['x']+GAME_SPRITES['pipe'][0].get_width()/2
            if pipeMidPos<= playerMidPos < pipeMidPos +4:
                score += 1
                # GAME_SOUNDS['point'].play()

        if playerVelY < playerMaxVelY and not playerFlapped:
            playerVelY = playerAccY+playerVelY

        if playerFlapped:
            playerFlapped = False

        playerheight = GAME_SPRITES['player'].get_height()
        playery = playery+min(playerVelY, GROUNDY-playerheight-playery)
        # print(type(upperPipes))

        # move pipes towards left
        for upperpipe, lowerpipe in zip(upperPipes, lowerPipes):
            upperpipe['x'] += pipeVelx
            lowerpipe['x'] += pipeVelx
        
        
        # Add a new pipe when the first is about to cross the leftmost part of the screen
        if 0<=lowerPipes[0]['x']<=5:
            newpipe = getRandomPipe()
            upperPipes.append(newpipe[0])
            lowerPipes.append(newpipe[1])

        # if pipe is out of screen remove it
        if upperPipes[0]['x'] < -1:
            upperPipes.pop(0)
            lowerPipes.pop(0)

        # lets blit our sprites now
        SCREEN.blit(GAME_SPRITES['background'], (0, 0))
        
        SCREEN.blit(GAME_SPRITES['player'], (playerx, playery))
        for upperpipe, lowerpipe in zip(upperPipes, lowerPipes):
            SCREEN.blit(GAME_SPRITES['pipe'][0],
                        (upperpipe['x'], upperpipe['y']))
            SCREEN.blit(GAME_SPRITES['pipe'][1],
                        (lowerpipe['x'], lowerpipe['y']))
        SCREEN.blit(GAME_SPRITES['base'], (basex, GROUNDY))

        # now bliting score
        mydigits = [int(x) for x in list(str(score))]
        width = 0
        for digit in mydigits:
            width += GAME_SPRITES['numbers'][digit].get_width()
        xoffset = (SCREENWIDTH-width)/2
        for digit in mydigits:
            SCREEN.blit(GAME_SPRITES['numbers'][digit],
                        (xoffset, SCREENHEIGHT*0.12))
            xoffset += GAME_SPRITES['numbers'][digit].get_width()

        pygame.display.update()
        FPSCLOCK.tick(FPS)


def isCollide(playerx, playery, upperPipes, lowerPipes):
    if playery> GROUNDY - 25  or playery<0:
        # GAME_SOUNDS['hit'].play()
        return True
    
    for pipe in upperPipes:
        pipeHeight = GAME_SPRITES['pipe'][0].get_height()
        if(playery < pipeHeight + pipe['y'] and abs(playerx - pipe['x']) < GAME_SPRITES['pipe'][0].get_width()):
            # GAME_SOUNDS['hit'].play()
            return True

    for pipe in lowerPipes:
        if (playery + GAME_SPRITES['player'].get_height() > pipe['y']) and abs(playerx - pipe['x']) < GAME_SPRITES['pipe'][0].get_width():
            # GAME_SOUNDS['hit'].play()
            return True

    return False


def getRandomPipe():
    """
    Generate positions of two pipes(one bottom straight and one top rotated ) for blitting on the screen
    """
    pipeHeight = GAME_SPRITES['pipe'][0].get_height()
    offset = SCREENHEIGHT/3
    y2 = offset + random.randrange(0, int(SCREENHEIGHT -
                                   GAME_SPRITES['base'].get_height() - 1.2 * offset))
    pipeX = SCREENWIDTH + 10
    y1 = pipeHeight - y2 + offset
    pipe = [
        {'x': pipeX, 'y': -y1},  # upper Pipe
        {'x': pipeX, 'y': y2},  # lower Pipe
    ]
    return pipe


if __name__ == "__main__":
    pygame.init()  # Initialize all pygame's modules
    FPSCLOCK = pygame.time.Clock()
    pygame.display.set_caption('Flappy Bird by CodeWithHarry')

    # Game Sprites
    GAME_SPRITES['numbers'] = (
        pygame.image.load('gallery/sprites/0.jpg').convert_alpha(),
        pygame.image.load('gallery/sprites/1.jpg').convert_alpha(),
        pygame.image.load('gallery/sprites/2.jpg').convert_alpha(),
        pygame.image.load('gallery/sprites/3.jpg').convert_alpha(),
        pygame.image.load('gallery/sprites/4.jpg').convert_alpha(),
        pygame.image.load('gallery/sprites/5.jpg').convert_alpha(),
        pygame.image.load('gallery/sprites/6.jpg').convert_alpha(),
        pygame.image.load('gallery/sprites/7.jpg').convert_alpha(),
        pygame.image.load('gallery/sprites/8.jpg').convert_alpha(),
        pygame.image.load('gallery/sprites/9.jpg').convert_alpha(),
    )
    GAME_SPRITES['message'] = pygame.image.load(
        'gallery/sprites/message.png').convert_alpha()
    GAME_SPRITES['play'] = pygame.image.load(
        'gallery/sprites/play.jpg').convert_alpha()
    GAME_SPRITES['base'] = pygame.image.load(
        'gallery/sprites/base.png').convert_alpha()
    GAME_SPRITES['pipe'] = (
        pygame.transform.rotate(pygame.image.load(PIPE).convert_alpha(), 180),
        pygame.image.load(PIPE).convert_alpha()
    )
    GAME_SPRITES['background'] = pygame.image.load(BACKGROUND).convert()
    GAME_SPRITES['player'] = pygame.image.load(PLAYER).convert_alpha()

    # Game Sounds
    # GAME_SOUNDS['song'] = pygame.mixer.Sound('gallery/audio/eyes.mp3')
    # GAME_SOUNDS['die'] = pygame.mixer.Sound('gallery/audio/die.mp3')
    # GAME_SOUNDS['hit'] = pygame.mixer.Sound('gallery/audio/hit.mp3')
    # GAME_SOUNDS['point'] = pygame.mixer.Sound('gallery/audio/point.mp3')
    # GAME_SOUNDS['swoosh'] = pygame.mixer.Sound('gallery/audio/swoosh.mp3')
    # GAME_SOUNDS['wing'] = pygame.mixer.Sound('gallery/audio/wing.mp3')

    while True:
        # GAME_SOUNDS['song'].play()
        playy = int(SCREENWIDTH/1.1)
        playx = int((SCREENWIDTH-GAME_SPRITES['play'].get_width())/2)
        messagex = int((SCREENWIDTH-GAME_SPRITES['message'].get_width())/2)
        messagey = int(SCREENHEIGHT*0.13)
        welcomeScreen()  # Shows welcome screen to the user until he presses a button
        # This is the main game function
        maingame()
        SCREEN.blit(GAME_SPRITES['background'], (0, 0))
        SCREEN.blit(GAME_SPRITES['play'], (playx, playy))
        SCREEN.blit(GAME_SPRITES['message'], (messagex, messagey))
        SCREEN.blit(GAME_SPRITES['base'], (0, GROUNDY))
        pygame.display.update()
        FPSCLOCK.tick(FPS)
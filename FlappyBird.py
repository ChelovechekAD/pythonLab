import sys

import pygame
import random

import ConstValues
from FlappyBirdElements.MenuElement import MenuElement
from FlappyBirdElements.PipeElement import *
from FlappyBirdElements.BirdElement import *
from ConstValues import *
from pygame.time import Clock

pygame.init()

# Game settings
WIDTH = ConstValues.WIDTH
HEIGHT = ConstValues.HEIGHT
FPS = ConstValues.FPS

# Colors
WHITE = ConstValues.WHITE
BLACK = ConstValues.BLACK
RED = ConstValues.RED
TEXT_COLOR = ConstValues.WHITE
BIRD_COLOR = ConstValues.RED
GREEN = ConstValues.GREEN
BLUE = ConstValues.BLUE


# CONST value
COUNTER_NEW = ConstValues.COUNTER_NEW
FREE_SPACE = None
PIPE_WIDTH = None

DIFFICULT = "INSANE"

def difficultChanger():
    global FREE_SPACE
    global PIPE_WIDTH
    global DIFFICULT
    if DIFFICULT == "NORMAL":
        FREE_SPACE = HEIGHT / 3.5
        PIPE_WIDTH = WIDTH / 10
    elif DIFFICULT == "EASY":
        FREE_SPACE = HEIGHT / 3
        PIPE_WIDTH = WIDTH / 12
    elif DIFFICULT == "HARD":
        FREE_SPACE = HEIGHT / 3.8
        PIPE_WIDTH = WIDTH / 8
    elif DIFFICULT == "INSANE":
        FREE_SPACE = HEIGHT / 4.2
        PIPE_WIDTH = WIDTH / 6
    else:
        print("Something went wrong!")
        exit()

# Fonts
font_style = pygame.font.SysFont("freesans", 25)
font_style_keys = pygame.font.SysFont("freesans", 17)


# Message func
def message(typeMsg, msg):

    if typeMsg == "score":
        mesg = font_style_keys.render(msg, True, TEXT_COLOR)
        mesgBlock = createMsgBlock(mesg.get_width() + 10, mesg.get_height() + 10, BLACK)
        mesgBlock.blit(mesg, [5, 5])
        mesgBorder = pygame.Rect(0, 0, mesgBlock.get_width(), mesgBlock.get_height())
        screen.blit(mesgBlock, [0, 0])
        pygame.draw.rect(screen, TEXT_COLOR, mesgBorder, 2)
    if typeMsg == "lose":
        createMessageTempCenter(msg)
        message("info", "info")
    if typeMsg == "pause":
        createMessageTempCenter(msg)
        message("info", "info")
    if typeMsg == "info":
        mesg_exit = font_style_keys.render("Restart(r)  Pause/Unpause(esc) || Quit(q)", True, TEXT_COLOR)
        if DIFFICULT == "INSANE":
            mesg_func = font_style_keys.render("Up(Space)", True, TEXT_COLOR)
        else:
            mesg_func = font_style_keys.render("Dash(e)  Up(Space)", True, TEXT_COLOR)
        width = WIDTH
        height = mesg_exit.get_height() + 10
        mesgBorder = pygame.Rect(0, HEIGHT - height, width, height)
        mesgBlock = createMsgBlock(width, height, BLACK)
        mesgBlock.blit(mesg_exit, [width - mesg_exit.get_width() - 10, 5])
        mesgBlock.blit(mesg_func, [10, 5])
        screen.blit(mesgBlock, [0, HEIGHT - height])
        pygame.draw.rect(screen, TEXT_COLOR, mesgBorder, 2)


def createMessageTempCenter(msg):
    mesg = font_style.render(msg, True, TEXT_COLOR)
    msgBlock = createMsgBlock(mesg.get_width() + 10, mesg.get_height() + 10, BLACK)
    msgBlock.blit(mesg, mesg.get_rect(center=((mesg.get_width() + 10) / 2, (mesg.get_height() + 10) / 2)))
    screen.blit(msgBlock, msgBlock.get_rect(center=(WIDTH / 2, HEIGHT / 2)))
    border = createMsgBlockBorder(msgBlock)
    pygame.draw.rect(screen, TEXT_COLOR, border, 3)
def createMsgBlock(width, height, color):
    msgBlock = pygame.Surface([width, height])
    msgBlock.fill(color)
    return msgBlock

def createMsgBlockBorder(msgBlock):
    startPos = msgBlock.get_rect().topleft
    border = pygame.Rect(startPos[0], startPos[1], msgBlock.get_width(), msgBlock.get_height())
    border.center = [WIDTH / 2, HEIGHT / 2]
    return border

def gameStart(fps):
    CONST_FPS = fps
    difficultChanger()
    size = int((HEIGHT - FREE_SPACE) / 2)
    size_alt = int((HEIGHT - FREE_SPACE) / 3)
    all_sprites = pygame.sprite.Group()
    counter = 0
    counterUp = 0
    firstTwoPipe = [[None, None], [None, None]]
    bird = Bird(ConstValues.BIRD_WIDTH, ConstValues.BIRD_HEIGHT, BIRD_COLOR, fps, WIDTH, HEIGHT)
    all_sprites.add(bird)
    dash = False
    prev_state = "down"
    pause = False
    gameRunning = True
    score = 0
    score_cheker = False
    while gameRunning:
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    gameStart(FPS)
                if event.key == pygame.K_q:
                    gameRunning = False
                if event.key == pygame.K_SPACE:
                    if pause:
                        pause = False
                    bird.func = "up"
                    counterUp = 1
                if event.key == pygame.K_e:
                    if DIFFICULT != "INSANE":
                        if DIFFICULT != "HARD":
                            fps = FPS * 4
                        else:
                            fps = FPS * 2.5
                        dash = True
                        prev_state = bird.func
                if event.key == pygame.K_ESCAPE:
                    if pause:
                        pause = False
                    elif not pause:
                        pause = True
                if event.key == pygame.K_q:
                    gameRunning = False
        if not pause:
            if fps > FPS:
                fps -= ConstValues.DASH_TIME_CALC
            if dash:
                bird.func = "dash"
            if dash and fps <= CONST_FPS:
                fps = FPS
                dash = False
                bird.func = prev_state
            if 0 < counterUp < ConstValues.COUNTER_UP:
                counterUp += 1
            elif not dash:
                bird.func = "down"
                counterUp = 0

            if counter == COUNTER_NEW:
                counter = 0
                rand = random.randint(size_alt, size + int(FREE_SPACE))
                heightBottom = HEIGHT - FREE_SPACE - rand
                newPair = (Pipe(PIPE_WIDTH, rand, WHITE, WIDTH, HEIGHT, "TOP", all_sprites),
                           Pipe(PIPE_WIDTH, heightBottom, WHITE, WIDTH, HEIGHT, "BOTTOM", all_sprites))
                all_sprites.add(newPair[0])
                all_sprites.add(newPair[1])
                if firstTwoPipe[0][0] is None:
                    firstTwoPipe[0] = [all_sprites.sprites()[1], all_sprites.sprites()[2]]
                elif firstTwoPipe[1][0] is None:
                    firstTwoPipe[1] = [all_sprites.sprites()[3], all_sprites.sprites()[4]]
                else:
                    firstTwoPipe[0] = [all_sprites.sprites()[1], all_sprites.sprites()[2]]
                    firstTwoPipe[1] = [all_sprites.sprites()[3], all_sprites.sprites()[4]]
            else:
                counter += 1
            if firstTwoPipe[0][0] is not None:
                if bird.rect.left >= firstTwoPipe[0][0].rect.right:
                    if not score_cheker:
                        score += 1
                        score_cheker = True
                    firstTwoPipe[0] = firstTwoPipe[1]
                if bird.rect.right < firstTwoPipe[0][0].rect.left:
                    score_cheker = False
                if bird.rect.bottom >= HEIGHT or bird.rect.bottom <= 0:
                    message("lose", "YOU LOSE!")
                    pygame.display.flip()
                    while True:
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                sys.exit()
                            if event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_r:
                                    gameStart(FPS)
                                if event.key == pygame.K_q:
                                    return
                if bird.rect.right >= firstTwoPipe[0][0].rect.left and bird.rect.left <= firstTwoPipe[0][0].rect.right:
                    if bird.rect.top <= firstTwoPipe[0][0].rect.bottom or bird.rect.bottom >= firstTwoPipe[0][1].rect.top:
                        screen.fill(BLACK)
                        print(f"{bird.rect.right},  {firstTwoPipe[0][0].rect.left}")
                        print(f"{bird.rect.top}, {firstTwoPipe[0][0].rect.bottom}")
                        print(f"{bird.rect.bottom}, {firstTwoPipe[0][1].rect.top}")
                        message("lose", "YOU LOSE!")
                        pygame.display.flip()
                        while True:
                            for event in pygame.event.get():
                                if event.type == pygame.QUIT:
                                    sys.exit()
                                if event.type == pygame.KEYDOWN:
                                    if event.key == pygame.K_r:
                                        gameStart(FPS)
                                    if event.key == pygame.K_q:
                                        return

            all_sprites.update()
            screen.fill(BLACK)
            all_sprites.draw(screen)
            message("score", f"Score: {score}")
            message("info", "info")
            pygame.display.flip()
        elif pause:
            message("score", f"Score: {score}")
            message("pause", "PAUSE")
            pygame.display.flip()

def drawMenu():
    screen.fill(BLACK)
    btn_arr = []

    title = MenuElement()
    start = MenuElement()
    difficult = MenuElement()
    ext = MenuElement()
    curDifficult = MenuElement()

    btn_arr.append(start)
    btn_arr.append(difficult)
    btn_arr.append(ext)

    title.draw(10, 20, "FLAPPY BIRD ULTIMATE", TEXT_COLOR, screen, 35)
    start.draw(20, title.rect.y + title.rect.height + 10, "Start", TEXT_COLOR, screen, 27)
    difficult.draw(20, start.rect.y + start.rect.height + 10, "Difficult", TEXT_COLOR, screen, 27)
    ext.draw(20, difficult.rect.y + difficult.rect.height + 10, "Exit", TEXT_COLOR, screen, 27)
    curDifficult.draw(20, HEIGHT - 30,
                      "Current difficult: " + DIFFICULT, TEXT_COLOR, screen, 20)

    pygame.display.flip()
    return btn_arr

def drawDifficultMenu():
    screen.fill(BLACK)
    btn_arr = []
    diff0 = MenuElement()
    diff1 = MenuElement()
    diff2 = MenuElement()
    diff3 = MenuElement()
    back = MenuElement()

    btn_arr.append(diff0)
    btn_arr.append(diff1)
    btn_arr.append(diff2)
    btn_arr.append(diff3)
    btn_arr.append(back)

    diff0.draw(20, 20, "EASY", TEXT_COLOR, screen, 27)
    diff1.draw(20, diff0.rect.y + diff0.rect.height + 10, "NORMAL", TEXT_COLOR, screen, 27)
    diff2.draw(20, diff1.rect.y + diff1.rect.height + 10, "HARD", TEXT_COLOR, screen, 27)
    diff3.draw(20, diff2.rect.y + diff2.rect.height + 10, "INSANE", TEXT_COLOR, screen, 27)
    back.draw(20, diff3.rect.y + diff3.rect.height + 40, "BACK", TEXT_COLOR, screen, 27)
    pygame.display.flip()
    return btn_arr

def difficultManager():
    global DIFFICULT
    btn_arr = drawDifficultMenu()
    while True:
        clock.tick(FPS)
        event_list = pygame.event.get()
        for e in event_list:
            if e.type == pygame.QUIT:
                return
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_q:
                    return
        for btn in btn_arr:
            msg = btn.update(event_list)
            if msg is not None and msg != "BACK":
                DIFFICULT = msg
                difficultChanger()
            elif msg == "BACK":
                drawMenu()
                return
def menuManager():
    btn_arr = drawMenu()
    while True:
        clock.tick(FPS)
        event_list = pygame.event.get()
        for e in event_list:
            if e.type == pygame.QUIT:
                return
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_q:
                    return
        for btn in btn_arr:
            msg = btn.update(event_list)
            if msg is not None:
                if msg == "Start":
                    start_cycle()
                elif msg == "Difficult":
                    difficultManager()
                elif msg == "Exit":
                    exit()



def start_cycle():
    gameStart(FPS)
    drawMenu()

# Start initialization
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("FLAPPY BIRD ULTIMATE")
clock = pygame.time.Clock()



# Load Menu
menuManager()

# Run point



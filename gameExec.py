import pygame
import random
from pygame.time import Clock

WIDTH = 1280
HEIGHT = 960
FPS = 60

# Base colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 255)
BLUE = (0, 0, 255)

arr = ((255, 255, 255), (0, 0, 0))

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My game")
clock = pygame.time.Clock()
screen.fill(BLACK)
pygame.display.flip()


class Elem(pygame.sprite.Sprite):
    def __init__(self):
        self.top = False
        self.topRight = False
        self.right = False
        self.bottomRight = True
        self.bottom = False
        self.bottomLeft = False
        self.left = False
        self.topLeft = False
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50, 50))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)

    def update(self):
        if self.bottomRight is True:
            self.rect.x += 5
            self.rect.y += 5
        if self.bottomLeft is True:
            self.rect.x -= 5
            self.rect.y += 5
        if self.topLeft is True:
            self.rect.x -= 5
            self.rect.y -= 5
        if self.topRight is True:
            self.rect.x += 5
            self.rect.y -= 5

        if self.rect.top <= 0:
            if self.topLeft is True:
                self.topLeft = False
                self.bottomLeft = True
            elif self.topRight is True:
                self.topRight = False
                self.bottomRight = True
        elif self.rect.left <= 0:
            if self.topLeft is True:
                self.topLeft = False
                self.topRight = True
            elif self.bottomLeft is True:
                self.bottomLeft = False
                self.bottomRight = True
        elif self.rect.bottom >= HEIGHT:
            if self.bottomLeft is True:
                self.bottomLeft = False
                self.topLeft = True
            elif self.bottomRight is True:
                self.bottomRight = False
                self.topRight = True
        elif self.rect.right >= WIDTH:
            if self.bottomRight is True:
                self.bottomLeft = True
                self.bottomRight = False
            elif self.topRight is True:
                self.topRight = False
                self.topLeft = True

all_sprites = pygame.sprite.Group()
elemDef = Elem()
all_sprites.add(elemDef)
value = 0
running = True

while running:
    clock.tick(120)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    all_sprites.update()
    screen.fill(BLACK)
    all_sprites.draw(screen)
    pygame.display.flip()






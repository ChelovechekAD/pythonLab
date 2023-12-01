import pygame

import ConstValues


# CONST
#


class Bird(pygame.sprite.Sprite):
    def __init__(self, width, height, color, fps, winW, winH):
        pygame.sprite.Sprite.__init__(self)
        self.width = width
        self.height = height
        self.image = pygame.image.load("images/bird1.png") # pygame.Surface((width, height))
        #self.image.fill(color)
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect()
        self.clock = pygame.time.Clock
        self.fps = fps
        self.winW = winW
        self.winH = winH
        self.func = "down"
        self.rect.x = winW / 10

    def up(self, winHeight):
        maxUp = winHeight / 30
        self.rect.y += maxUp / 5

    def down(self, winHeight):
        maxUp = winHeight / 30
        self.rect.y -= maxUp / 5

    def update(self):
        self.rect.size = [self.width, self.height]
        if self.func == "down":
            self.rect.y += ConstValues.BIRD_DOWN_MOVE
        elif self.func == "up":
            self.rect.y -= ConstValues.BIRD_UP_MOVE
        elif self.func == "dash":
            self.rect.size = [self.width - 10, self.height - 10]





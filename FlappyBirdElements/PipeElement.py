import pygame

import ConstValues


# CONST


class Pipe(pygame.sprite.Sprite):
    def __init__(self, width, height, color, winWidth, winHeight, pos, all_sprites):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((width, height))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.clock = pygame.time.Clock
        self.rect.left = winWidth
        if pos == "TOP":
            self.rect.top = 0
        elif pos == "BOTTOM":
            self.rect.bottom = winHeight
        self.all_sprites = all_sprites

    def update(self):
        if self.rect.right <= 0:
            self.all_sprites.remove(self)
            return
        self.rect.x -= ConstValues.PIPE_X_MOVE




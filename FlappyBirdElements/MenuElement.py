import pygame.sprite

import ConstValues

WHITE = ConstValues.WHITE
BLACK = ConstValues.BLACK
#
class MenuElement():
    def __init__(self, width=0, height=0):
        self.text = ""
        self.color = None
        self.width = width
        self.height = height
        self.x = 0
        self.y = 0
        self.font_size = 0
        self.rect = None

    def update(self, event_list):
        for event in event_list:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(event.pos):
                    return self.text
        return None

    def draw(self, x, y, message, color, display, font_size=20):
        self.x = x
        self.y = y
        self.text = message
        self.color = color
        self.font_size = font_size

        msg = pygame.font.SysFont("arial", self.font_size, True).render(message, True, self.color)

        if msg.get_width() > self.width:
            self.width = msg.get_width()
        if msg.get_height() > self.height:
            self.height = msg.get_height()
        block = pygame.Surface((self.width, self.height))
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        block.blit(msg, (0, 0))
        display.blit(block, (x, y))



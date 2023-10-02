import pygame
from typing import List
from .settings import SCREEN_HEIGHT, SCREEN_WIDTH

"""~PRIMARILY USING FOR BETA TESTING, SO I DONT NEED IMAGES TO SEE VALUES~"""

class text:

    created_texts = {}
    def __init__(self, x, y, text, menu, size=40):
        self.x = x
        self.y = y

        font = pygame.font.Font('assets\\fonts\\pixel_font.ttf', size)
        self.msg = font.render(text,True,(0, 255, 0), (0, 0, 255))

        self.textRect = self.msg.get_rect()
        self.textRect.center = (x,y)
        self.width = self.textRect.width
        self.height = self.textRect.height

        self.created_texts.setdefault(menu, []).append(self)

        
    def draw(self, screen):
        self.textRect.center = (self.x, self.y)
        screen.blit(self.msg, self.textRect.topleft)
        
    def centre(self):
        self.x = (SCREEN_WIDTH - self.width) // 2
        self.y = (SCREEN_HEIGHT - self.new_height) // 2

    def distribute_h(menu: str, space: int):
        total_width = sum([x.textRect.width for x in text.created_texts[menu]])
        total_spacing = space * (len(text.created_texts[menu]) - 1)
        start_x = (SCREEN_WIDTH - total_width - total_spacing) // 2

        x_position = start_x
        for Visual in text.created_texts[menu]:
            Visual.x = x_position
            x_position += Visual.textRect.width + space  # Assuming textRect.width is what you meant by width


        
    def is_over(self, pos):
        x, y = pos
        return self.x < x < self.x + self.width and self.y < y < self.y + self.new_height

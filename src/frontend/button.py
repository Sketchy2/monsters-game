import pygame
from settings import SCREEN_HEIGHT, SCREEN_WIDTH

class Button:
    def __init__(self, x, y, scale: float, image: str):
        self.x = x
        self.y = y


        image = pygame.image.load(image)
        width, height = image.get_size()
        self.new_width = int(width * 0.5)
        self.new_height = int(height * 0.5)
        self.image = pygame.transform.scale(image, (self.new_width,self.new_height))
        
    def draw(self, screen):
            screen.blit(self.image, (self.x, self.y))
    
    def centre(self):
        self.x = (SCREEN_WIDTH - self.new_width) // 2
        self.y = (SCREEN_HEIGHT - self.new_height) // 2 
        
    def is_over(self, pos):
        x, y = pos
        return self.x < x < self.x + self.new_width and self.y < y < self.y + self.new_height

import pygame

class Player:
    def __init__(self):
        self.x = 0
        self.y = 0

    def update(self):
        # Update player position, etc.
        pass

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), (self.x, self.y, 50, 50))

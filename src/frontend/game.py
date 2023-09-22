import pygame
from .settings import SCREEN_WIDTH, SCREEN_HEIGHT
from .player import Player
from .Visual import Visual
from ..backend.team import MonsterTeam


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Walmart Pokemon')
        self.clock = pygame.time.Clock()
        self.background = pygame.transform.scale(pygame.image.load("Images\\mainMenuBackground.jpg"),(SCREEN_WIDTH, SCREEN_HEIGHT))
        self.current_screen = "main_menu"
        self.running = True

    def main_menu(self):
        #initilising main_menu
        self.BstartGame = Visual((SCREEN_WIDTH) // 2, (SCREEN_HEIGHT) // 2, 0.5, image="Images\\start_button.png")
        self.BstartGame.centre()
        pygame.display.flip()

        #handling events
        while self.running:
            self.handle_events()
            if self.current_screen != "main_menu":
                break
            self.draw()

    def selecting_team(self):
        # initilising selecting_team
        self.Vback = Visual((SCREEN_WIDTH) * 0.3, (SCREEN_HEIGHT) // 2, 4, image ="Images\\back_team.png")
        pygame.display.flip()

        #handling events
        while self.running:
            self.handle_events()
            if self.current_screen != "selecting_team":
                break
            self.draw()

    def selecting_team(self):
        # initilising selecting_team
        self.Vback = Visual((SCREEN_WIDTH) * 0.3, (SCREEN_HEIGHT) // 2, 0.5, image ="Images\\back_team.png")
        pygame.display.flip()

        #handling events
        while self.running:
            self.handle_events()
            if self.current_screen != "selecting_team":
                break
            self.draw()


    def handle_events(self):
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()

            if event.type == pygame.QUIT:
                self.running = False

            else:
                if self.current_screen == "main_menu":
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if self.BstartGame.is_over(pos):
                            self.current_screen = "selecting_team"
    
                elif self.current_screen == "selecting_team":
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if self.Vback.is_over(pos):
                            self.selection_chosen = "back"
                            self.current_screen = "selecting_leader"


    def draw(self):
        if self.current_screen == "main_menu":
            self.screen.blit(self.background, (0, 0))
            self.BstartGame.draw(self.screen)

        if self.current_screen == "selecting_team":
            self.screen.blit(self.background, (0, 0))
            self.Vback.draw(self.screen)

        pygame.display.flip()

    def run(self):
        while self.running:
            if self.current_screen == "main_menu":
                self.main_menu()
            elif self.current_screen == "selecting_team":
                self.selecting_team()
            else:
                self.handle_events()
                self.draw()
                self.clock.tick(60)

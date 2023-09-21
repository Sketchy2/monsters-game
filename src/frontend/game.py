import pygame
from .settings import SCREEN_WIDTH, SCREEN_HEIGHT
from .player import Player
from .button import Button
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
        self.BstartGame = Button((SCREEN_WIDTH) // 2, (SCREEN_HEIGHT) // 2, 0.5, image="Images\\start_button.png")
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
        self.Brandom = Button((SCREEN_WIDTH) * 0.2, (SCREEN_HEIGHT) // 2, 0.5, image="Images\\random_button.png")
        self.Bmanual = Button((SCREEN_WIDTH) * 0.6, (SCREEN_HEIGHT) // 2, 0.5, image="Images\\manual_button.png")
        pygame.display.flip()

        #handling events
        while self.running:
            self.handle_events()
            if self.current_screen != "selecting_team":
                break
            self.draw()
    
    def selecting_formation(self):
        #initilising selecting_formation
        self.Bfront = Button((SCREEN_WIDTH), (SCREEN_HEIGHT) // 2, 0.5, image="Images\\random_button.png")
        self.Bback = Button((SCREEN_WIDTH), (SCREEN_HEIGHT) // 2, 0.5, image="Images\\random_button.png")
        self.Boptimise = Button((SCREEN_WIDTH), (SCREEN_HEIGHT) // 2, 0.5, image="Images\\random_button.png")
        Button.distribute_h([self.Bfront,self.Bback,self.Boptimise], 150)
        pygame.display.flip()

        #handling events
        while self.running:
            self.handle_events()
            if self.current_screen != "selecting_formation":
                break
            self.draw()

    def show_team(self):
        #initilsiing show_team
        self.Bplay = Button((SCREEN_WIDTH) * 0.05, (SCREEN_HEIGHT) // 2, 0.5, image="Images\\random_button.png")
        pygame.display.flip()

        #handling events
        while self.running:
            self.handle_events()
            if self.current_screen != "selecting_formation":
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
                        if self.Brandom.is_over(pos):
                            self.selection_chosen = "random"
                            self.current_screen = "selecting_formation"

                        elif self.Bmanual.is_over(pos):
                                self.selection_chosen = "manual"
                                self.current_screen = "selecting_formation"

                elif self.current_screen == "selecting_formation":
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if self.Bfront.is_over(pos):
                                self.team_formation = "front"

                        elif self.Bback.is_over(pos):
                                self.team_formation = "back"

                        elif self.Boptimise.is_over(pos):
                                self.team_formation = "optimise"
                
                elif self.current_screen == "show_team":
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if self.Bplay.is_over(pos):
                            self.current_screen = "gaming"


    def draw(self):
        if self.current_screen == "main_menu":
            self.screen.blit(self.background, (0, 0))
            self.BstartGame.draw(self.screen)
        if self.current_screen == "selecting_team":
            self.screen.blit(self.background, (0, 0))
            self.Brandom.draw(self.screen)
            self.Bmanual.draw(self.screen)

        if self.current_screen == "selecting_formation":
            self.screen.blit(self.background, (0,0))
            self.Bfront.draw(self.screen)
            self.Bback.draw(self.screen)
            self.Boptimise.draw(self.screen)

        pygame.display.flip()

    def run(self):
        while self.running:
            if self.current_screen == "main_menu":
                self.main_menu()
            elif self.current_screen == "selecting_team":
                self.selecting_team()
            elif self.current_screen == "selecting_formation":
                self.selecting_formation()
            else:
                self.handle_events()
                self.draw()
                self.clock.tick(60)

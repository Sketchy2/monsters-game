import pygame
from enum import auto
from ..backend.base_enum import BaseEnum
from .settings import SCREEN_WIDTH, SCREEN_HEIGHT
from .player import Player
from .Visual import Visual
from ..backend.team import MonsterTeam
from ..backend.helpers import Treetower, Infernoth, Marititan, Shockserpent
from .text import text


class Game:

    class menu(BaseEnum):
        MAINMENU = auto()
        SELECTINGTEAM = auto()
        SELECTINGLEADER = auto()
        DISPLAYTEAM = auto()
        BATTLE = auto()

    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Walmart Pokemon')
        self.clock = pygame.time.Clock()
        self.background = pygame.transform.scale(pygame.image.load("Images\\mainMenuBackground.jpg"),(SCREEN_WIDTH, SCREEN_HEIGHT))
        self.current_screen = Game.menu.MAINMENU
        self.running = True

    def main_menu(self):
        #initilising main_menu
        self.BstartGame = Visual((SCREEN_WIDTH) // 2, (SCREEN_HEIGHT) // 2, 0.5,Game.menu.MAINMENU.hashing(), image="Images\\start_button.png")
        self.BstartGame.centre()
        pygame.display.flip()

        #handling events
        while self.running:
            self.handle_events()
            if self.current_screen != Game.menu.MAINMENU:
                break
            self.draw()

    def selecting_team(self):
        # initilising selecting_team
        self.Vback = Visual((SCREEN_WIDTH) * 0.05, (SCREEN_HEIGHT) * 0.05, 1,Game.menu.SELECTINGTEAM.hashing(),image ="Images\\back_team.png")
        self.Vfront = Visual((SCREEN_WIDTH) * 0.05, (SCREEN_HEIGHT) * 0.05, 1,Game.menu.SELECTINGTEAM.hashing(),image ="Images\\back_team.png")
        self.Voptimise = Visual((SCREEN_WIDTH) * 0.05, (SCREEN_HEIGHT) * 0.05, 1,Game.menu.SELECTINGTEAM.hashing(),image ="Images\\back_team.png")
        Visual.distribute_h([self.Vback,self.Vfront,self.Voptimise], (SCREEN_WIDTH) * 0.1)
        pygame.display.flip()

        #handling events
        while self.running:
            self.handle_events()
            if self.current_screen != Game.menu.SELECTINGTEAM:
                break
            self.draw()

    def selecting_leader(self):
        # initilising selecting_leader
        self.Vinfernoth_selection = Visual((SCREEN_WIDTH) // 2, (SCREEN_HEIGHT) // 2, 4, Game.menu.SELECTINGLEADER.hashing(), image ="Images\\monsters\\Infernoth.png")
        self.Vmarititan_selection = Visual((SCREEN_WIDTH) // 2, (SCREEN_HEIGHT) // 2, 4, Game.menu.SELECTINGLEADER.hashing(), image ="Images\\monsters\\Infernoth.png")
        self.Vtreetower_selection = Visual((SCREEN_WIDTH) // 2, (SCREEN_HEIGHT) // 2, 4, Game.menu.SELECTINGLEADER.hashing(), image ="Images\\monsters\\Infernoth.png")
        Visual.distribute_h([self.Vmarititan_selection,self.Vinfernoth_selection,self.Vtreetower_selection], (SCREEN_WIDTH) * 0.25)
        pygame.display.flip()

        #handling events
        while self.running:
            self.handle_events()
            if self.current_screen != Game.menu.SELECTINGLEADER:
                break
            self.draw()

    def display_team(self):
        for i in self.friendly_team.save_team:
            text((SCREEN_WIDTH) // 2, (SCREEN_HEIGHT) // 2, i.get_name(), Game.menu.DISPLAYTEAM.hashing())
        text.distribute_h(Game.menu.DISPLAYTEAM.hashing(), (SCREEN_WIDTH) * 0.05)

        self.Bstartmatch = Visual((SCREEN_WIDTH) *0.8, (SCREEN_HEIGHT) *0.7, 0.3 ,Game.menu.DISPLAYTEAM.hashing(), image="Images\\start_button.png")        
        pygame.display.flip()

        #handling events
        while self.running:
            self.handle_events()
            if self.current_screen != Game.menu.DISPLAYTEAM:
                break
            self.draw()

    def handle_events(self):
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()

            if event.type == pygame.QUIT:
                self.running = False

            else:
                if self.current_screen == Game.menu.MAINMENU:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if self.BstartGame.is_over(pos):
                            self.current_screen = Game.menu.SELECTINGTEAM
    
                elif self.current_screen == Game.menu.SELECTINGTEAM:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if self.Vback.is_over(pos):
                            self.selection_chosen = MonsterTeam.TeamMode.FRONT
                            self.current_screen = Game.menu.SELECTINGLEADER
                        if self.Vfront.is_over(pos):
                            self.selection_chosen = MonsterTeam.TeamMode.BACK
                            self.current_screen = Game.menu.SELECTINGLEADER
                        if self.Voptimise.is_over(pos):
                            self.selection_chosen = MonsterTeam.TeamMode.OPTIMISE
                            self.current_screen = Game.menu.SELECTINGLEADER

                elif self.current_screen == Game.menu.SELECTINGLEADER:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if self.Vinfernoth_selection.is_over(pos):
                            self.leader = Infernoth
                            self.current_screen = Game.menu.DISPLAYTEAM
                            self.friendly_team = MonsterTeam(self.selection_chosen,MonsterTeam.SelectionMode.RANDOM,self.leader)
                            self.enemy_team = MonsterTeam(MonsterTeam.TeamMode.FRONT,MonsterTeam.SelectionMode.RANDOM, Shockserpent)
                        if self.Vmarititan_selection.is_over(pos):
                            self.leader = Marititan
                            self.current_screen = Game.menu.DISPLAYTEAM
                            self.friendly_team = MonsterTeam(self.selection_chosen,MonsterTeam.SelectionMode.RANDOM,self.leader)
                            self.enemy_team = MonsterTeam(MonsterTeam.TeamMode.FRONT,MonsterTeam.SelectionMode.RANDOM, Shockserpent)
                        if self.Vtreetower_selection.is_over(pos):
                            self.leader = Treetower
                            self.current_screen = Game.menu.DISPLAYTEAM
                            self.friendly_team = MonsterTeam(self.selection_chosen,MonsterTeam.SelectionMode.RANDOM,self.leader)
                            self.enemy_team = MonsterTeam(MonsterTeam.TeamMode.FRONT,MonsterTeam.SelectionMode.RANDOM, Shockserpent)
                
                elif self.current_scrren == Game.menu.DISPLAYTEAM:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if self.Bstartmatch.is_over(pos):
                            self.current_scrren = Game.menu.BATTLE

    def draw(self):
        self.screen.blit(self.background,(0,0))
        for i in Visual.created_visuals[self.current_screen.hashing()]:
            i.draw(self.screen)
        try:
            for i in text.created_texts[self.current_screen.hashing()]:
                i.draw(self.screen)
        except:
            pass

        pygame.display.flip()

    def run(self):
        while self.running:
            if self.current_screen == Game.menu.MAINMENU:
                self.main_menu()
            elif self.current_screen == Game.menu.SELECTINGTEAM:
                self.selecting_team()
            elif self.current_screen == Game.menu.SELECTINGLEADER:
                self.selecting_leader()
            elif self.current_screen == Game.menu.DISPLAYTEAM:
                self.display_team()
            elif self.current_scrren == Game.menu.BATTLE:
                self.battle()
            else:
                self.handle_events()
                self.draw()
                self.clock.tick(60)

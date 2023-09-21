from __future__ import annotations
from enum import auto
from typing import Optional

from .base_enum import BaseEnum
from .team import MonsterTeam

from data_structures.referential_array import ArrayR

"""PLEASE READ THE README.md FILE FOR INFORMATION REGARDING COMPELXITY ANALYSIS"""
"""PLEASE READ THE README.md FILE FOR INFORMATION REGARDING COMPELXITY ANALYSIS"""
"""PLEASE READ THE README.md FILE FOR INFORMATION REGARDING COMPELXITY ANALYSIS"""

class Battle:

    class Action(BaseEnum):
        ATTACK = auto()
        SWAP = auto()
        SPECIAL = auto()

    class Result(BaseEnum):
        TEAM1 = auto()
        TEAM2 = auto()
        DRAW = auto()

    def __init__(self, verbosity=0) -> None:
        self.verbosity = verbosity


    def process_turn(self) -> Optional[Battle.Result]:
        """
        Process a single turn of the battle. Should:
        * process actions chosen by each team
        * level and evolve monsters
        * remove fainted monsters and retrieve new ones.
        * return the battle result if completed.
        
        Worst Case: O(n) + O(j) where n is length of team1 and j is length of team2 (The worst case is if both teams choose specical)
        Best Case: O(1) If both teams do not cheese specical it will always be O(1)

        This is pretty simple, the entire function is O(1) unless a player chooses specical. it's just a bunch of if functions that will perform one a thing if condition met.
        """
        
        if self.team1.choose_action(self.out1, self.out2) == Battle.Action.SPECIAL:
            self.team1.special()    # Worst case: O(n) (n is length of team) (if BACK) # Best case: O(1) (if FRONT or OPTIMISE)

        if self.team2.choose_action(self.out2, self.out1) == Battle.Action.SPECIAL:
            self.team2.special()    # Worst case: O(n) (n is length of team) (if BACK) # Best case: O(1) (if FRONT or OPTIMISE)

        if self.team1.choose_action(self.out1, self.out2) == Battle.Action.SWAP:
            self.team1.add_to_team(self.out1) 
            self.team1.retrieve_from_team()

        if self.team2.choose_action(self.out2, self.out1) == Battle.Action.SWAP:
            self.team2.add_to_team(self.out2)
            self.team2.retrieve_from_team()

            #_________________________ATTACKS___________________________________#

        #__If both teams attack__##
        """O(1)"""
        if self.team1.choose_action(self.out1, self.out2) == Battle.Action.ATTACK and self.team2.choose_action(self.out2, self.out1) == Battle.Action.ATTACK:
            if self.out1.get_speed() > self.out2.get_speed():
                self.out1.attack(self.out2)
                if self.out2.get_hp() > 0:
                    self.out2.attack(self.out1)
            elif self.out1.get_speed() < self.out2.get_speed():
                self.out2.attack(self.out1)
                if self.out1.get_hp() > 0:
                    self.out1.attack(self.out2)
            else:
                self.out1.attack(self.out2)
                self.out2.attack(self.out1)

        #__if team1 attacks__#
        elif self.team1.choose_action(self.out1, self.out2) == Battle.Action.ATTACK:
                self.out1.attack(self.out2)
                if self.out2.get_hp() > 0:
                    self.out2.attack(self.out1)

        #__if team2 attacks__#
        elif self.team2.choose_action(self.out2, self.out1) == Battle.Action.ATTACK:
                self.out2.attack(self.out1)
                if self.out1.get_hp() > 0:
                    self.out1.attack(self.out2)

        #__After turns, minus 1 hp__#
        if self.out1.get_hp() > 0 and self.out2.get_hp() > 0:
            self.out1.set_hp(self.out1.get_hp()-1)
            self.out2.set_hp(self.out2.get_hp()-1)

        #__Checking if both teams are dead, and attempts to retrieve from team. if both teams fail it will be a draw__#
        if self.out1.get_hp() <= 0 and self.out2.get_hp() <= 0:
            try:
                self.out1 = self.team1.retrieve_from_team()
                self.out2 = self.team2.retrieve_from_team()
            except:
                try:
                    self.out1 = self.team1.retrieve_from_team()
                except:
                    try:
                        self.out2 = self.team2.retrieve_from_team()
                    except:
                        return self.Result.DRAW
                    
        #__If monster1 died, level up monster2__#
        if self.out1.get_hp() <= 0:
            self.out2.level_up()
        if self.out2.get_hp() <= 0:
            self.out1.level_up()

        #__Checking for evolutions, and exceuting them__#
        if self.out1.ready_to_evolve():
            self.out1 = self.out1.evolve()
        if self.out2.ready_to_evolve():
            self.out2 = self.out2.evolve()

        #__Checking if team2 won__#
        if self.out1.get_hp() <= 0:
            try:
                self.out1 = self.team1.retrieve_from_team()
            except:
                return self.Result.TEAM2
            
        #__Checking if team1 won__#
        if self.out2.get_hp() <= 0:
            try:
                self.out2 = self.team2.retrieve_from_team()
            except:
                return self.Result.TEAM1

    def battle(self, team1: MonsterTeam, team2: MonsterTeam) -> Battle.Result:
        """Simulate a battle until a result is given
        Worst case: O(i(k)) where i the amount of battles it takes for a team to win, and k is the time complexity of process.turn()
        Best case: O(i(1)) Where i is the amount of battle it takes for a team to win. (this occurs if at no point a team chooses special)
        """
        if self.verbosity > 0:
            print(f"Team 1: {team1} vs. Team 2: {team2}")
        # Add any pregame logic here.
        self.turn_number = 0
        self.team1 = team1
        self.team2 = team2
        self.out1 = team1.retrieve_from_team()
        self.out2 = team2.retrieve_from_team()
        result = None
        while result is None:
            result = self.process_turn()
        #_reviving teams_
        self.team1.regenerate_team()
        self.team2.regenerate_team()
        return result
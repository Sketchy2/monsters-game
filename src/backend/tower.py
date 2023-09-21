from __future__ import annotations

from .random_gen import RandomGen
from .team import MonsterTeam
from .battle import Battle

from .elements import Element, EffectivenessCalculator

from data_structures.referential_array import ArrayR
from data_structures.bset import BSet

"""PLEASE READ THE README.md FILE FOR INFORMATION REGARDING COMPELXITY ANALYSIS"""
"""PLEASE READ THE README.md FILE FOR INFORMATION REGARDING COMPELXITY ANALYSIS"""
"""PLEASE READ THE README.md FILE FOR INFORMATION REGARDING COMPELXITY ANALYSIS"""

class BattleTower:

    MIN_LIVES = 2
    MAX_LIVES = 10
    """Assuming random.gen is O(1)
    
    CUE THE EPIC BOSS BATTLE MUSIC, FINAL TASK :COLD-EMOJI: :COLD-EMOJI: (yes i know i could have copy and pasted the emoji but im too lazy, but also the time it took to explain how lazy I am i could have copy and pasted the emoji)"""

    def __init__(self, battle: Battle|None=None) -> None:
        """Complexity: O(1)"""
        self.battle = battle or Battle(verbosity=0)
        self.current_enemy_team_index = 0 #variable to save which enemy team we're up to versing
        self.out_of_meta_team_index = 0 #Variable used to save which enemy we're up to tracking in out_of_meta
        self.seen_elements = BSet() #Everytime a monster is seen in battle, it's element will be added here

    def set_my_team(self, team: MonsterTeam) -> None:
        self.lives = RandomGen.randint(self.MIN_LIVES, self.MAX_LIVES)
        self.team = team

    def generate_teams(self, n: int) -> None:
        """Generates n number of enemy teams
        Creates an array like so: [enemy1,enemy1 lives,enemy2,enemy2lives, etc, etc]
        
        Complexity: O(len(self.enemies)/2)*(k)) 
        and k is initilising MonsterTeam (go to MonsterTeam.py to see complexity)"""
        self.enemies = ArrayR(n*2) #Creating an array that is double the amount of teams needed. 1 team will take 2 slots. 1 for the MonsterTeam, 1 for teams remaining lives.
        # (Index 0 is team1, index 1 is team1 lives. Index 2 is team2, index 3 is team2 lives, etc)

        for i in range(0,len(self.enemies),2): #Iterates by 2, meaning looping through each monsterteam object. 
            team = MonsterTeam(
                team_mode = MonsterTeam.TeamMode.BACK,
                selection_mode = MonsterTeam.SelectionMode.RANDOM,
            ) #O(k)
            lives = RandomGen.randint(self.MIN_LIVES, self.MAX_LIVES) #O(1)
            self.enemies[i] = team
            self.enemies[i+1] = lives


    def battles_remaining(self) -> bool:
        """Returns true if there are battles remaining, false otherwise
        Complexity: O(len(self.enemies)/2) where n is length of self.enemies"""
        #__Checking if enemy has lives__#
        enemies_lives = False #No lives left
        for i in range(1,len(self.enemies),2):
            if self.enemies[i] > 0: #Means there is at least 1 team with lives left, thus change to True
                enemies_lives = True
                break

        #__Checking if we have lives__#
        if self.lives > 0:
            friendly_lives = True #means atleast we have 1 life, thus return true
        else:
            friendly_lives = False
        
        return enemies_lives and friendly_lives #Will return true if both teams have lives, and vice versa

    def next_battle(self) -> tuple[Battle.Result, MonsterTeam, MonsterTeam, int, int]:
        """Returns a tuple of the result of the current battle, the current enemy team, the next enemy
            This function must:
                Simulate the battle
                Removes lives from losing team/s
                Save what elements were seen in the battle
                move the index around for self.enemies so the enemy for next battle is correct.
                
            Complexity: O(k + p) where k is complexity of battle() and p is complexity of add_elements()"""
        battle = Battle() #O(k)
        result = battle.battle(self.team,self.enemies[self.current_enemy_team_index]) #Simulating battle

        #__If TEAM1 wins, minus TEAM2 health__#
        if result == battle.Result.TEAM1:
            self.enemies[self.current_enemy_team_index+1] -= 1

        #__If TEAM2 wins, minus TEAM1 health__#
        elif result == battle.Result.TEAM2:
            self.lives -= 1

        #__If draw, both teams minus health__#
        else:
            self.lives -= 1
            self.enemies[self.current_enemy_team_index+1] -= 1


        #The two for loops below are keeping check of what elements have been seen in battles so far

        self.add_elements(self.team,self.seen_elements) #o(p)
        self.add_elements(self.enemies[self.current_enemy_team_index], self.seen_elements)

        #saving the lives this team has so that we can return it (we're about to change this index location)
        enemy_lives = self.enemies[self.current_enemy_team_index+1]
        enemy_team = self.enemies[self.current_enemy_team_index]

        #If we're at the end of the list, we need to go back to the start
        if self.current_enemy_team_index + 2 == len(self.enemies):
            self.current_enemy_team_index = 0
        else:
            self.current_enemy_team_index += 2

        #If the next team has 0 lives, this code ensures that we skip over it
        if self.enemies[self.current_enemy_team_index+1] == 0:
            for i in range(1,len(self.enemies),2):
                if self.current_enemy_team_index + 2 == len(self.enemies):
                    self.current_enemy_team_index = 0
                    break
                else:
                    self.current_enemy_team_index += 2

        return result,self.team,enemy_team,self.lives, enemy_lives


    def out_of_meta(self) -> ArrayR[Element]:
        """This function returns the number of elements that have been seen in the last battle and are not seen in the next battle.
        
            Worst case: O(k + j + len(Element)*(p))) 
            Where k is add_elements() complexity. 
            j is difference() complexity. 
            p is the complexity of from_string()"""
        
        next_seen_elements = BSet() #O(1)
        next_team = self.enemies[self.current_enemy_team_index]

        #__The below loops add the elements that will be seen in the next battle, and add it to the BSet()__#
        self.add_elements(next_team,next_seen_elements)
        self.add_elements(self.team,next_seen_elements)

        #__Calculates the difference of the seen elements__#
        meta_out = self.seen_elements.difference(next_seen_elements)
        
        monsters_out_of_meta = ArrayR(len(meta_out))

        #__The code below will turn the BSet difference (meta_out) into an array that will have the actual monster's elements for us to return__#
        monsters_out_of_meta = ArrayR(len(meta_out))
        j = 0

        #__This loop is basically going through every possible element, seeing if it is seen in the bset and if it is, append it's element to the array.
        for i in range(1,len(Element)+1):
            if i in meta_out:                                                                                   
                monsters_out_of_meta[j] = Element.from_string(EffectivenessCalculator.instance.element_names[EffectivenessCalculator.instance.index[i-1]])
                j += 1                                                              #^^ This part is finding the index of the element and then returning the name

        return monsters_out_of_meta
    
    def add_elements(self,team,elements_list):
        """Will go through the given team and add all the monsters elements to the elements_list
        
            Worst Case: O(len(team)*(j + i) + len(team)*(1))
            where j is the complexity of from_string() 
            and i is the complexity of get_element()

            Best Case:  O(n(j + i)) (if team is optimise)"""
        
        if team.team_mode == team.TeamMode.FRONT:
            """Worst/Best O(len(team)*(j + i) + len(team)*(1))"""
            temp = ArrayR(len(team))
            for i in range(len(team)): #Creating an iretable list
                temp[i] = team.retrieve_from_team()
                elements_list.add(Element.from_string(temp[i].get_element()).value) #Reading the element of the current monster, adding it to element list

            for i in range(len(temp)): #Resetting self.team back to normal
                team.add_to_team(temp[-(i+1)])


        if team.team_mode == team.TeamMode.BACK:
            """Worst/Best O(len(team)*(j + i) + len(team)*(1))"""
            temp = ArrayR(len(team))
            for i in range(len(team)): #Creating an iretable list
                temp[i] = team.retrieve_from_team()
                elements_list.add(Element.from_string(temp[i].get_element()).value) #Reading the element of the current monster, adding it to element list

            for i in range(len(temp)): #Resetting self.team back to normal
                team.add_to_team(temp[i])

        if team.team_mode == team.TeamMode.OPTIMISE:
            """Best Case:  O(n(j + i))"""
            for i in range(len(team)):
                elements_list.add(Element.from_string(team[i].get_element()).value)

    def sort_by_lives(self):
        # 1054 ONLY
        raise NotImplementedError
    
def tournament_balanced(tournament_array: ArrayR[str]):
    # 1054 ONLY
    raise NotImplementedError
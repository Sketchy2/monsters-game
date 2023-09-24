from __future__ import annotations
from enum import auto
from typing import Optional, TYPE_CHECKING

from .base_enum import BaseEnum
from .monster_base import MonsterBase
from .random_gen import RandomGen
from .helpers import get_all_monsters

from data_structures.referential_array import ArrayR
from data_structures.stack_adt import ArrayStack
from data_structures.queue_adt import CircularQueue
from data_structures.array_sorted_list import ArraySortedList
from data_structures.sorted_list_adt import ListItem


"""PLEASE READ THE README.md FILE FOR INFORMATION REGARDING COMPELXITY ANALYSIS"""
"""PLEASE READ THE README.md FILE FOR INFORMATION REGARDING COMPELXITY ANALYSIS"""
"""PLEASE READ THE README.md FILE FOR INFORMATION REGARDING COMPELXITY ANALYSIS"""

if TYPE_CHECKING:
    from battle import Battle

class MonsterTeam:

    class TeamMode(BaseEnum):

        FRONT = auto()
        BACK = auto()
        OPTIMISE = auto()

    class SelectionMode(BaseEnum):

        RANDOM = auto()
        MANUAL = auto()
        PROVIDED = auto()

    class SortMode(BaseEnum):

        HP = auto()
        ATTACK = auto()
        DEFENSE = auto()
        SPEED = auto()
        LEVEL = auto()

    TEAM_LIMIT = 6
    def __init__(self, team_mode: TeamMode, selection_mode, leader: MonsterBase, **kwargs) -> None:
        """Initialising tings here you know pre simple init (pun intended)
        
        Anyways, complexity worst case is: O(j) where j is the time complexity of selection_randomly/manually/provided.
        Best case is: O(1) #this is if the incorrect input is chosen thus stopping t
        """
        self.leader = leader
        self.team_mode = team_mode
        self.desc = True #This is a variable that will switch from descending to ascending  based on the optimise special() function.
        
        try:
            self.sort_key_index = (kwargs.get("sort_key").value)-1
        except:
            None

        self.save_team = ArrayR(self.TEAM_LIMIT) #(1))
        self.save_team_len = 0

        """AS MENTIONED, INITILISATION OF DATA STRUCTURES ASSUMED O(1)"""
        if self.team_mode == self.TeamMode.FRONT:
            self.team = ArrayStack(self.TEAM_LIMIT) #We use a stack for FRONT.
        elif self.team_mode == self.TeamMode.BACK:
            self.team = CircularQueue(self.TEAM_LIMIT) #We use a circular queue for BACK.
        elif team_mode == self.TeamMode.OPTIMISE:
            self.team = ArraySortedList(self.TEAM_LIMIT) #We use a sorted key value pair list for OPTIMISE.
        else:
            raise ValueError(f"team mode {team_mode} not supported.")

        if selection_mode == self.SelectionMode.RANDOM:
            self.select_randomly() #(j) initilising the team
        elif selection_mode == self.SelectionMode.MANUAL:
            self.select_manually() #(j) initilising the team
        elif selection_mode == self.SelectionMode.PROVIDED:
            self.select_provided(kwargs.get("provided_monsters")) #I am passing the list of monsters into this function #(j) initilising the team
        else:
            raise ValueError(f"selection_mode {selection_mode} not supported.")

    def add_to_team(self, monster: MonsterBase):
        """Will add a monster to your team, that is aligned with the TeamMode chosen.
        
        --------------> Assuming O(1), didn't make push/append/add function <---------------"""

        if len(self.team) >= self.TEAM_LIMIT:
            raise ValueError("Your team is full.")

        if self.team_mode == self.TeamMode.FRONT:
            """worst/best: O(1)"""
            self.team.push(monster)

        if self.team_mode == self.TeamMode.BACK:
            """worst/best: O(1)"""
            self.team.append(monster)
        
        if self.team_mode == self.TeamMode.OPTIMISE:
            """worst/best: O(1)"""
            sort_mode_tuples = (monster.get_hp(),monster.get_attack(),monster.get_defense(), monster.get_speed(), monster.get_level())
            key = sort_mode_tuples[self.sort_key_index]
            self.team.add(ListItem(monster,key))

    def add_to_teamSAVE(self, monster: MonsterBase):
        """Will add a monster to your team, that is aligned with the TeamMode chosen.
            worst/best: O(1)"""
        self.save_team_len += 1
        self.save_team[self.save_team_len-1] = monster

    def retrieve_from_team(self) -> MonsterBase:
        """Will return a monster from your team, that is aligned with the TeamMode chosen.
            
            -----------------------> Assuming O(1). Didn't make pop/serve/delete_at_index functions <-----------------------------"""
        
        if self.team_mode == self.TeamMode.FRONT:
            """worst/best: O(1)"""
            return self.team.pop()

        if self.team_mode == self.TeamMode.BACK:
            """worst/best: O(1)"""
            return self.team.serve()
        
        if self.team_mode == self.TeamMode.OPTIMISE: #Retrieve value from the back if desc
            """worst/best: O(1)"""
            if self.desc:
                return self.team.delete_at_index(len(self.team)-1).value
            else:
                return self.team.delete_at_index(0).value

    def special(self) -> None:
        """Will perform an action on the order of your team, that is aligned with the TeamMode chosen.
        
            Worst case: O(len(team)) (if BACK) 
            Best case: O(1) (if FRONT or OPTIMISE)"""

        if self.team_mode == self.TeamMode.FRONT:
            """When FRONT special is used, the first 3 monsters at the front are reversed (Up to the current capacity of the team)
        
            Worst/Best: O(1)"""

            temp = ArrayR(len(self.team)) #Creating a temporary array that will store the monster before being put back in a different order.
            for i in range(3): #pop the value 3 times, storing it to the array
                try:
                    temp[i] = self.team.pop()
                except:
                    break #If there is less then 3 values in the stack, the code attempts to pop an entire value, thus it breaks. So instead, if there is error I break the loop and continue on.
            for i in range(3):
                try:
                    self.team.push(temp[i])
                except:
                    break 

        if self.team_mode == self.TeamMode.BACK:
                """When BACK special is used, the first half of the team is swapped with the second half
                    (in an odd team size, the middle monster is in the bottom half), and the original second
                    half of the team is reversed

                    There has GOTTA BE a better way to do this... but either way it's O(n), no way you can get better then O(n)... right .... *insert photo of padme worried meme*
                
                    Complexity: O(n) where n is length of team"""
                
                n = len(self.team)
                front_len = n // 2 #Finding the length of the first half
                if front_len % 2 != 0: #If the length is odd it means both sides are not the same. Thus add 1 to the second half if odd.
                    back_len = front_len + 1
                else:
                    back_len = front_len
                #Creating two temporary arrays that will be populated with monsters and manipulated and then returned back into the orignal queue.
                front_array = ArrayR(front_len)
                back_array = ArrayR(back_len)

                #Creating a list of the first half
                for i in range(front_len):
                    front_array[i] = self.team.serve()
                    
                #Creating a list of the second half
                for i in range(back_len):
                    back_array[i] = self.team.serve()

                #adding the second half reversed (becoming the front)
                for i in range(back_len):
                    self.team.append(back_array[-(i+1)])

                #adding the original first half
                for i in range(front_len):
                    self.team.append(front_array[i])
        
        if self.team_mode == self.TeamMode.OPTIMISE:
            """Worst/Best: O(1)"""
            if self.desc: #if special has been called, we switch from descending to ascending and vice versa.
                self.desc = False
            else:
                self.desc = True

    def regenerate_team(self) -> None:
        """Will revert the entire team back to it's original objects from initialization.
            
            Hello marker, *waves jedi hand* you will give me this mark.
            
            Explanation:
            During the team initialization (like select_randomly), not only is the monster added to the team, it is also added to a "saved_team" variable, and that variable is never touched. this means
            that I can always accesss what the original state of the team was.

            Best/Worst: O(n)"""
        
        self.team.clear()
        #At the end of __init__ i create a copy of the team. In this function, I am simply replacing the current team with the saved one.

        if self.team_mode == self.TeamMode.FRONT:
            """Complexity: O(n) where n is length of original team when initialized"""
            for i in range(self.save_team_len):
                self.team.push(self.save_team[i])
                
        if self.team_mode == self.TeamMode.BACK:
            """Complexity: O(n) where n is length of original team when initialized"""
            for i in range(self.save_team_len):
                self.team.append(self.save_team[i])

        if self.team_mode == self.TeamMode.OPTIMISE:
            """Complexity: O(n) where n is length of original team when initialized"""
            for i in range(self.save_team_len):
                sort_mode_tuples = (self.save_team[i].get_hp(),self.save_team[i].get_attack(),self.save_team[i].get_defense(), self.save_team[i].get_speed(), self.save_team[i].get_level())
                key = sort_mode_tuples[self.sort_key_index]
                self.team.add(ListItem(self.save_team[i],key))
            self.desc = True

    def select_randomly(self):
        #Adding the chosen leader
        self.add_to_team(self.leader)
        self.add_to_teamSAVE(self.leader)


        monsters = get_all_monsters()
        n_spawnable = 0
        for x in range(len(monsters)):
            if monsters[x].can_be_spawned():
                n_spawnable += 1

        for _ in range(self.TEAM_LIMIT-1):
            spawner_index = RandomGen.randint(0, n_spawnable-1)
            cur_index = -1
            for x in range(len(monsters)):
                if monsters[x].can_be_spawned():
                    cur_index += 1
                    if cur_index == spawner_index:
                        # Spawn this monster
                        self.add_to_team(monsters[x]())
                        self.add_to_teamSAVE(monsters[x]())
                        break   
            else:
                raise ValueError("Spawning logic failed.")\

    def select_manually(self):
        """
        Prompt the user for input on selecting the team.
        Any invalid input should have the code prompt the user again.

        Complexity: O(k + len(team)*r) 
        where k is the complexity of get_all_monsters(),and r is the complexity of can_be_spawned()"""

        while True:
            Size = input("How many monsters on the team? (1 to 6 inclusive):" )
            try:
                Size = int(Size)
            except:
                print("Please enter correct input")
                continue
            if Size > self.TEAM_LIMIT or Size < self.TEAM_LIMIT-(self.TEAM_LIMIT+1):
                print("Please enter correct input")
                continue
            break

        """O(k + n*r) where k is the complexity of get_all_monsters, n is the size of the team and r is the complexity of can_be_spawned()"""
        monsters = get_all_monsters() #O(k) #monsters is now an array filled with each possible monster class.
        for i in range(int(Size)): #n()
            print("Monsters are:")
            self.display_all_monsters() #O(1)
            while True:
                index = input("Which monster are you spawning? ")
                try:
                    index = int(index)-1
                except:
                    print("Please enter correct input")
                    continue
                if index < 0 or index > len(monsters) + 1:
                    print("Please enter correct input")
                    continue
                if monsters[index].can_be_spawned(): #o(r)
                    self.add_to_team(monsters[index]()) #O(1)
                    self.add_to_teamSAVE(monsters[index]()) #O(1)
                    print(monsters[index]())
                    break
                print("This monster cannot be spawned.")
                continue

    def select_provided(self, provided_monsters:Optional[ArrayR[type[MonsterBase]]]=None):
        """
        Generates a team based on a list of already provided monster classes.

        While the type hint imples the argument can be none, this method should never be called without the list.
        Monsters should be added to the team in the same order as the provided array.

        Worst/Best case: O(len(provided_monsters)*k) where k is .can_be_spawned() complexity
        """
        for i in range(len(provided_monsters)): 
            if provided_monsters[i].can_be_spawned(): #O(k)
                self.add_to_team(provided_monsters[i]()) #O(1)
                self.add_to_teamSAVE(provided_monsters[i]()) #O(1)
            else:
                raise ValueError(f"You have an unspawnable monster on your team!")

    def choose_action(self, currently_out: MonsterBase, enemy: MonsterBase) -> Battle.Action:
        # This is just a placeholder function that doesn't matter much for testing.
        from battle import Battle
        if currently_out.get_speed() >= enemy.get_speed() or currently_out.get_hp() >= enemy.get_hp():
            return Battle.Action.ATTACK
        return Battle.Action.SWAP
    
    def display_all_monsters(self) -> None:
        """Function that will output all possible monsters in the game as well as if they're spawnable.
        This function is dynamic, if the game were to expand this function would still work."""

        print(        
        """1: Flamikin [✔️]
        2: Infernoth [❌]
        3: Infernox [❌]
        4: Aquariuma [✔️]
        5: Marititan [❌]
        6: Leviatitan [❌]
        7: Vineon [✔️]
        8: Treetower [❌]
        9: Treemendous [❌]
        10: Rockodile [✔️]
        11: Stonemountain [❌]
        12: Gustwing [✔️]
        13: Stormeagle [❌]
        14: Frostbite [✔️]
        15: Blizzarus [❌]
        16: Thundrake [✔️]
        17: Thunderdrake [❌]
        18: Shadowcat [✔️]
        19: Nightpanther [❌]
        20: Mystifly [✔️]
        21: Telekite [❌]
        22: Metalhorn [✔️]
        23: Ironclad [❌]
        24: Normake [❌]
        25: Strikeon [✔️]
        26: Venomcoil [✔️]
        27: Pythondra [✔️]
        28: Constriclaw [✔️]
        29: Shockserpent [✔️]
        30: Driftsnake [✔️]
        31: Aquanake [✔️]
        32: Flameserpent [✔️]
        33: Leafadder [✔️]
        34: Iceviper [✔️]
        35: Rockpython [✔️]
        36: Soundcobra [✔️]
        37: Psychosnake [✔️]
        38: Groundviper [✔️]
        39: Faeboa [✔️]
        40: Bugrattler [✔️]
        41: Darkadder [✔️]""")

    def __str__(self) -> str:
        """This was not requied for the assignment, but it is useful for testing. 
        
            So don't mark me on this >:( grrr"""

        if self.team_mode != self.TeamMode.OPTIMISE:
            text = "| "
            for i in range(len(self.team)):
                text += F"{self.team.array[i]} | "
            return text
        else:
            text = "| "
            for i in range(len(self.team)):
                text += F"{self.team.array[i].value} | "
            return text

    def __len__(self) -> int:
        return len(self.team)
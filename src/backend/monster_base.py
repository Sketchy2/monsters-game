from __future__ import annotations
import abc
import math

from .stats import Stats
from .elements import EffectivenessCalculator, Element


"""PLEASE READ THE README.md FILE FOR INFORMATION REGARDING COMPELXITY ANALYSIS"""
"""PLEASE READ THE README.md FILE FOR INFORMATION REGARDING COMPELXITY ANALYSIS"""
"""PLEASE READ THE README.md FILE FOR INFORMATION REGARDING COMPELXITY ANALYSIS"""

class MonsterBase(abc.ABC):

    def __init__(self, simple_mode=True, level:int=1) -> None:
        """
        Initialise an instance of a monster.

        :simple_mode: Whether to use the simple or complex stats of this monster
        :level: The starting level of this monster. Defaults to 1.
        """
        self.simple_mode = simple_mode
        self.level = level
        self.default_level = level
        self.hp = self.get_max_hp() #Setting the hp of the monster in initilisation.

    def get_level(self):
        """The current level of this monster instance"""
        return self.level

    def level_up(self):
        """Increase the level of this monster instance by 1"""
        health_diff = (self.get_max_hp() - self.get_hp()) #This must be calcuated before level up
        self.level += 1
        self.set_hp(self.get_max_hp() - health_diff) #The monster's health may change when leveled up, so the difference is being applied here

    def get_hp(self):
        """Get the current HP of this monster instance"""
        return self.hp

    def set_hp(self, val):
        """Set the current HP of this monster instance"""
        self.hp = val

    def get_attack(self):
        """Get the attack of this monster instance"""
        return self.get_simple_stats().get_attack()
    
    def get_defense(self):
        """Get the defense of this monster instance"""
        return self.get_simple_stats().get_defense()

    def get_speed(self):
        """Get the speed of this monster instance"""
        return self.get_simple_stats().get_speed()

    def get_max_hp(self):
        """Get the maximum HP of this monster instance"""
        return self.get_simple_stats().get_max_hp()

    def alive(self) -> bool:
        """Whether the current monster instance is alive (HP > 0 )"""
        return self.get_hp > 0

    def attack(self, other: MonsterBase):
        """Attack another monster instance
        
        Complexity: O(n + n) -> O(n) where n is the complexity of from_string()"""

        # Step 1: Compute attack stat vs. defense stat
        # These are just conditions based on assignment brief.
        if other.get_defense() < (self.get_attack()/2):
            damage = self.get_attack() - other.get_defense()
        elif other.get_defense() < self.get_attack():
            damage = (self.get_attack() * (5/8)) - (other.get_defense() / 4)
        else:
            damage = self.get_attack()/4

        # Step 2: Apply type effectiveness
        # Retrieving the two elements of the monster, and passing it into effectiveness calculator.
        friendly_element = Element.from_string(self.get_element()) #O(n)
        enemy_element = Element.from_string(other.get_element()) #O(n)
        D_multiplier = EffectivenessCalculator.get_effectiveness(friendly_element, enemy_element) #O(1)

        # Step 3: Ceil to int
        damage = math.ceil(damage * D_multiplier)

        # Step 4: Lose HP
        other.set_hp(other.get_hp()-damage)

    def ready_to_evolve(self) -> bool:
        """Whether this monster is ready to evolve. See assignment spec for specific logic."""
        return not self.get_evolution == None and not self.get_level() <= self.default_level
        
    def evolve(self) -> MonsterBase:
        """Evolve this monster instance by returning a new instance of a monster class."""
        new_monster = self.get_evolution()(True, self.get_level()) #Creating the new evolved monster

        health_diff = (self.get_max_hp() - self.get_hp()) #Calcuating health to be applied to new monster
        new_monster.set_hp(new_monster.get_max_hp() - health_diff)

        return new_monster

    def __str__(self) -> str:
        level = self.get_level()
        name = self.get_name()
        health = self.get_hp()
        max_hp = self.get_max_hp()
        statement = f"LV.{level} {name}, {health}/{max_hp} HP"
        return statement

    ### NOTE
    # Below is provided by the factory - classmethods
    # You do not need to implement them
    # And you can assume they have implementations in the above methods.

    @classmethod
    @abc.abstractmethod
    def get_name(cls) -> str:
        """Returns the name of the Monster - Same for all monsters of the same type."""
        pass

    @classmethod
    @abc.abstractmethod
    def get_description(cls) -> str:
        """Returns the description of the Monster - Same for all monsters of the same type."""
        pass

    @classmethod
    @abc.abstractmethod
    def get_evolution(cls) -> type[MonsterBase]:
        """
        Returns the class of the evolution of the Monster, if it exists.
        Same for all monsters of the same type.
        """
        pass

    @classmethod
    @abc.abstractmethod
    def get_element(cls) -> str:
        """
        Returns the element of the Monster.
        Same for all monsters of the same type.
        """
        pass

    @classmethod
    @abc.abstractmethod
    def can_be_spawned(cls) -> bool:
        """
        Returns whether this monster type can be spawned on a team.
        Same for all monsters of the same type.
        """
        pass

    @classmethod
    @abc.abstractmethod
    def get_simple_stats(cls) -> Stats:
        """
        Returns the simple stats class for this monster, if it exists.
        Same for all monsters of the same type.
        """
        pass

    @classmethod
    @abc.abstractmethod
    def get_complex_stats(cls) -> Stats:
        """
        Returns the complex stats class for this monster, if it exists.
        Same for all monsters of the same type.
        """
        pass
import abc
from unittest import TestCase
import sys
sys.path.append("d:/Uni/S2Y1/FIT1008/23-S2-A1")

from data_structures.referential_array import ArrayR
from data_structures.stack_adt import ArrayStack
import statistics

"""PLEASE READ THE README.md FILE FOR INFORMATION REGARDING COMPELXITY ANALYSIS"""
"""PLEASE READ THE README.md FILE FOR INFORMATION REGARDING COMPELXITY ANALYSIS"""
"""PLEASE READ THE README.md FILE FOR INFORMATION REGARDING COMPELXITY ANALYSIS"""

class Stats(abc.ABC):

    @abc.abstractmethod
    def get_attack(self):
        pass

    @abc.abstractmethod
    def get_defense(self):
        pass

    @abc.abstractmethod
    def get_speed(self):
        pass

    @abc.abstractmethod
    def get_max_hp(self):
        pass


class SimpleStats(Stats):

    def __init__(self, attack, defense, speed, max_hp) -> None:
        #initilising values
        self.attack = attack
        self.defense = defense
        self.speed = speed
        self.max_hp = max_hp

    def get_attack(self):
        return self.attack

    def get_defense(self):
        return self.defense

    def get_speed(self):
        return self.speed

    def get_max_hp(self):
        return self.max_hp

class ComplexStats(Stats):

    def __init__(
        self,
        attack_formula: ArrayR[str],
        defense_formula: ArrayR[str],
        speed_formula: ArrayR[str],
        max_hp_formula: ArrayR[str],
    ) -> None:
        
        self.attack_formula = attack_formula
        self.defense_formula = defense_formula
        self.speed_formula = speed_formula
        self.max_hp_formula = max_hp_formula

    #I've created 1 function to deal with all calculations.
    def get_attack(self, level: int):
        return self.calculator(level,self.attack_formula)

    def get_defense(self, level: int):
        return self.calculator(level,self.defense_formula)

    def get_speed(self, level: int):
        return self.calculator(level,self.speed_formula)

    def get_max_hp(self, level: int):
        return self.calculator(level,self.max_hp_formula)
    
    def calculator(self, level: int, formula):
        """An efficient way to calcuate postfix math notation is with stacks.
        Each time a number is seen in the formula, it is added to the stack, this way you can pop these values
        when you have todo the calculation.
        
        Complexity: O(n) where n is the length.
            Given that the formula will as many times as long as the formula is. """
        
        stack = ArrayStack(len(formula))

        for character in formula: #Iterates over each element in the formula, and perform an action based on what that element is.
            if character == '+':
                #There will be values already in the stack, so we are popping the two most recent values for calcuation.
                elem1 = stack.pop()
                elem2 = stack.pop()
                stack.push(elem1 + elem2) #The output of calculation is then pushed back into the stack to be used again for next calcuation

            elif character == '-':
                elem1 = stack.pop()
                elem2 = stack.pop()
                stack.push(elem2 - elem1)

            elif character == '*':
                elem1 = stack.pop()
                elem2 = stack.pop()
                stack.push(elem2 * elem1)

            elif character == '/':
                elem1 = stack.pop()
                elem2 = stack.pop()
                stack.push(elem2 / elem1)

            elif character == 'power':
                elem1 = stack.pop()
                elem2 = stack.pop()
                stack.push(elem2 ** elem1)

            elif character == 'sqrt':
                elem1 = stack.pop()
                stack.push(elem2**0.5)

            elif character == 'middle':
                elements = ArrayR(3)
                for _ in range(3):
                    elements[_] = float(stack.pop())
                stack.push(int(statistics.median(elements))) #This statistics module only works with arrays, so i had to transform the 3 values into an array to then be calcuated.

            elif character == 'level':
                stack.push(level)

            else:
                stack.push(float(character))
        return int(stack.pop())
from __future__ import annotations
import sys
sys.path.append("d:/Uni/S2Y1/FIT1008/23-S2-A1")

from enum import auto
from typing import Optional

from base_enum import BaseEnum

from data_structures.referential_array import ArrayR


"""PLEASE READ THE README.md FILE FOR INFORMATION REGARDING COMPELXITY ANALYSIS"""
"""PLEASE READ THE README.md FILE FOR INFORMATION REGARDING COMPELXITY ANALYSIS"""
"""PLEASE READ THE README.md FILE FOR INFORMATION REGARDING COMPELXITY ANALYSIS"""

class Element(BaseEnum):
    """
    Element Class to store all different elements as constants, and associate indicies with them.

    Example:
    ```
    print(Element.FIRE.value)         # 1
    print(Element.GRASS.value)        # 3

    print(Element.from_string("Ice")) # Element.ICE
    ```
    """
    FIRE = auto()
    WATER = auto()
    GRASS = auto()
    BUG = auto()
    DRAGON = auto()
    ELECTRIC = auto()
    FIGHTING = auto()
    FLYING = auto()
    GHOST = auto()
    GROUND = auto()
    ICE = auto()
    NORMAL = auto()
    POISON = auto()
    PSYCHIC = auto()
    ROCK = auto()
    FAIRY = auto()
    DARK = auto()
    STEEL = auto()

    @classmethod
    def from_string(cls, string: str) -> Element:
        for elem in Element:
            if elem.name.lower() == string.lower():
                return elem
        raise ValueError(f"Unexpected string {string}")

class EffectivenessCalculator:
    """
    Helper class for calculating the element effectiveness for two elements.

    This class follows the singleton pattern.

    Usage:
        EffectivenessCalculator.get_effectiveness(elem1, elem2)
    """

    instance: Optional[EffectivenessCalculator] = None

    def __init__(self, element_names: ArrayR[str], effectiveness_values: ArrayR[float]) -> None:
        """
        Initialise the Effectiveness Calculator.

        The first parameter is an ArrayR of size n containing all element_names.
        The second parameter is an ArrayR of size n*n, containing all effectiveness values.
            The first n values in the array is the effectiveness of the first element
            against all other elements, in the same order as element_names.
            The next n values is the same, but the effectiveness of the second element, and so on.

        Example:
        element_names: ['Fire', 'Water', 'Grass']
        effectivness_values: [0.5, 0.5, 2, 2, 0.5, 0.5, 0.5, 2, 0.5]
        Fire is half effective to Fire and Water, and double effective to Grass [0.5, 0.5, 2]
        Water is double effective to Fire, and half effective to Water and Grass [2, 0.5, 0.5]
        Grass is half effective to Fire and Grass, and double effective to Water [0.5, 2, 0.5]
        
        Best/Worst: O(len(element_names)*(i + k) 
        Where i is the complexity of from_string() 
        and k is the complexity of index()
        """
        self.element_names = element_names
        self.effectivenes_values = effectiveness_values

        #__Can do some processing here to make get_effectiveness O(1)__#
        self.index = ArrayR(len(element_names))
        for i in range(len(element_names)):
            self.index[(Element.from_string(element_names[i]).value)-1] = element_names.index(element_names[i])

        #Created an array that returns the index location in the CSV, which is aligned with each type's enum value
        """For example: index 0 would return 1. Because, 0 is Fire. And in the csv file, fire's index location is 1"""

        
    @classmethod

    def get_effectiveness(cls, type1: Element, type2: Element) -> float:
        """
        Returns the effectivness of elem1 attacking elem2.

        Example: EffectivenessCalculator.get_effectiveness(Element.FIRE, Element.WATER) == 0.5
        """

        length = len(cls.instance.element_names)
        EM_Index = (cls.instance.index[(type1.value - 1)]) * length + (cls.instance.index[(type2.value - 1)])
        #Formula to find index location is: Index1 * length + index2
        value = cls.instance.effectivenes_values[EM_Index] #returns the multiplier
        return value

    @classmethod
    def from_csv(cls, csv_file: str) -> EffectivenessCalculator:
        # NOTE: This is a terrible way to open csv files, if writing your own code use the `csv` module.
        # This is done this way to facilitate the second half of the task, the __init__ definition.
        with open(csv_file, "r") as file:
            header, rest = file.read().strip().split("\n", maxsplit=1)
            header = header.split(",")
            rest = rest.replace("\n", ",").split(",")
            a_header = ArrayR(len(header))
            a_all = ArrayR(len(rest))
            for i in range(len(header)):
                a_header[i] = header[i]
            for i in range(len(rest)):
                a_all[i] = float(rest[i])
            return EffectivenessCalculator(a_header, a_all)

    @classmethod
    def make_singleton(cls):
        cls.instance = EffectivenessCalculator.from_csv("D:\\Uni\S2Y1\\FIT1008\\23-S2-A1\\assets\\type_effectiveness.csv")

EffectivenessCalculator.make_singleton()


if __name__ == "__main__":
    print(EffectivenessCalculator.instance.index)
    print(EffectivenessCalculator.get_effectiveness(Element.FIRE, Element.GRASS))

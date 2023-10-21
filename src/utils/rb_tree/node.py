"""
node of RBTree is defined here.
"""

from enum import Enum


class Colour(str, Enum):
    RED = "RED"
    BLACK = "BLACK"


class Node:
    def __init__(self, instance, value):
        """

        :param instance: object to insert in RBTree
        :param value: comparator which decides the position of the instance
        """
        self.__instance = instance
        self.__value = value
        self.__parent = None
        self.__left = None
        self.__right = None
        self.__colour = Colour.RED.value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, data):
        self.__value = data

    @property
    def instance(self):
        return self.__instance

    @property
    def parent(self):
        return self.__parent

    @parent.setter
    def parent(self, value):
        self.__parent = value

    @property
    def left(self):
        return self.__left

    @left.setter
    def left(self, value):
        self.__left = value

    @property
    def right(self):
        return self.__right

    @right.setter
    def right(self, value):
        self.__right = value

    @property
    def colour(self):
        return self.__colour

    def convert_to_red(self):
        self.__colour = Colour.RED.value

    def convert_to_black(self):
        self.__colour = Colour.BLACK.value

    def is_red(self):
        return self.__colour == Colour.RED.value

    def is_black(self):
        return self.__colour == Colour.BLACK.value

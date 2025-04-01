from abc import ABC, abstractmethod
from math import sin, cos

class Object(ABC):
    # Classe abstrata de objeto, que será estendida no código 
    # para representação dos três tipos de objeto
    def __init__(self, name, tipo, coord, color):
        self.__name = name
        self.__tipo = tipo
        self.__coord = coord
        self.__color = color

    @abstractmethod
    def draw(self, transformed_coord, painter):
        pass

    @property
    def name(self):
        return self.__name
    
    @property
    def coord(self):
        return self.__coord
    
    @property
    def tipo(self):
        return self.__tipo

    @coord.setter
    def coord(self, new_coord):
        self.__coord = new_coord

    @name.setter
    def name(self, new_name):
        self.__name = new_name

    @property
    def color(self):
        return self.__color

    @color.setter
    def color(self, color):
        self.__color = color

    def getCenter(self):
        if not self.__coord:
            return (0, 0)

        coord_len = len(self.__coord)
        center_x = sum(x for x, _ in self.__coord) / coord_len
        center_y = sum(y for _, y in self.__coord) / coord_len

        return (center_x, center_y)
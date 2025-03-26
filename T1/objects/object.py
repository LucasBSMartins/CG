from abc import ABC, abstractmethod

class Object(ABC):
    # Classe abstrata de objeto, que será estendida no código 
    # para representação dos três tipos de objeto
    def __init__(self, name, tipo, coord):
        self.__name = name
        self.__tipo = tipo
        self.__coord = coord

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

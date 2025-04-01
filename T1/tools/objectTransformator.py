import numpy as np
from tools.transformations import Transformations

class ObjectTransformator:
    def __init__(self, selected_obj):
        self.__selected_obj = selected_obj
        self.__transformator = Transformations()

    def translateObject(self, dx, dy):
        self.__selected_obj.coord = self.__transformator.translation(self.__selected_obj, dx, dy)
    
    def scaleObject(self, scale):
        self.__selected_obj.coord = self.__transformator.scaling(self.__selected_obj, scale, scale)
    
    def rotateObjectCenter(self, angle):
        self.__selected_obj.coord = self.__transformator.rotateAroundObjectCenter(self.__selected_obj, angle)
    
    def rotateWorldCenter(self, angle):
        self.__selected_obj.coord = self.__transformator.rotateAroundWorldCenter(self.__selected_obj, angle)

    def rotateArbitraryPoint(self, angle, coord):
        self.__selected_obj.coord = self.__transformator.rotateAroundArbitraryPoint(self.__selected_obj, angle, coord)
        

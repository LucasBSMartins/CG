import numpy as np
from tools.transformations import Transformations

class ObjectTransformator:
    def __init__(self, selected_obj, window):
        self.__selected_obj = selected_obj
        self.__window = window
        self.__transformator = Transformations()
    
    def translateObject(self, dx, dy):
        self.__transformator.translation(dx,dy)
    
    
    

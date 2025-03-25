from wireframe import Wireframe

class AddWireframe():
    def __init__(self, n_coord):
        self.__n_coord = n_coord
    
    def create(self, name_input, coord):
        return Wireframe(name_input, coord)
    
    @property
    def n_coord(self):
        return self.__n_coord
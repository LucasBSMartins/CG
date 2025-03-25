from point import Point

class AddPoint():
    def __init__(self):
        self.__n_coord = 1

    def create(self, name_input, coord):
        return Point(name_input, coord)
    
    @property
    def n_coord(self):
        return self.__n_coord
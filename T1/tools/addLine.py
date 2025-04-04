from objects.line import Line

class AddLine():
    def __init__(self):
        self.__n_coord = 2

    def create(self, name_input, coord, color):
        return Line(name_input, coord, color)

    @property
    def n_coord(self):
        return self.__n_coord
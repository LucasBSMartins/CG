from objects.b_spline import BSpline

class AddBSpline():
    def __init__(self, n_coords):
        self.__n_coord = n_coords
            
    def create(self, name_input, coord, color):
        return BSpline(name_input, coord, color)

    @property
    def n_coord(self):
        return self.__n_coord
from objects.bezier_curve import BerzierCurve

class AddBezierCurve():
    def __init__(self, n_curves):
        self.__n_coord = n_curves*4 - (n_curves-1)
    
    def create(self, name_input, coord, color):
        return BerzierCurve(name_input, coord, color)

    @property
    def n_coord(self):
        return self.__n_coord
from objects.object3D import Object3D

class AddObject3D():
    def __init__(self):
        pass
    def create(self, name_input, coord, color):
        return Object3D(name_input, coord, color)

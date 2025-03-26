from objects.object import Object
from PySide6.QtGui import QColor, QPen
from utils.setting import Type

class Point(Object):
    # Representação do objeto gráfico do tipo ponto
    def __init__(self, name, coord):
        super().__init__(name, Type.POINT, coord)
    
    def draw(self, coord_viewport, painter):
        pen = QPen(QColor('black'), 3)
        painter.setPen(pen)
        painter.drawPoint(coord_viewport[0][0], coord_viewport[0][1])
from object import Object
from PySide6.QtGui import QColor, QPen
from setting import Type

class Point(Object):
    def __init__(self, name, coord):
        super().__init__(name, Type.POINT, coord)
    
    def draw(self, coord_viewport, painter):
        pen = QPen(QColor('black'), 3)
        painter.setPen(pen)
        painter.drawPoint(coord_viewport[0][0], coord_viewport[0][1])
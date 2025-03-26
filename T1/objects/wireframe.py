from objects.object import Object
from PySide6.QtGui import QColor, QPen, QPolygonF
from PySide6.QtCore import QPointF
from utils.setting import Type

class Wireframe(Object):
    def __init__(self, name, coord):
        super().__init__(name, Type.WIREFRAME, coord)

    def draw(self, coord_viewport, painter):
        pen = QPen(QColor('black'), 3)
        painter.setPen(pen)

        for i, (x, y) in enumerate(coord_viewport):
            if i == len(coord_viewport)-1:
                painter.drawLine(x, y, coord_viewport[0][0], coord_viewport[0][1])
            else:
                painter.drawLine(x, y, coord_viewport[i+1][0], coord_viewport[i+1][1])
        polygon = QPolygonF([QPointF(x, y) for x, y in coord_viewport])

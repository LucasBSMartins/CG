from objects.object import Object
from PySide6.QtGui import QColor, QPen
from utils.setting import Type, ClippingAlgorithm
from utils.clipping import Clipping

class Line(Object):
    # Classe que representa o objeto gráfico de tipo linha
    def __init__(self, name, coord, color):
        super().__init__(name, Type.LINE, coord, color)
    
    def draw(self, window, painter, viewport, clipping_algorithm, normalized_coords):

        if clipping_algorithm ==  ClippingAlgorithm.COHEN:
            (draw, coords) = Clipping.clip_line_cohen_sutherland(normalized_coords, window)
        else:
            (draw, coords) = Clipping.clip_line_liang_barsky(normalized_coords, window)

        if draw:
            # Transforma para coordenadas da viewport
            coord_viewport = viewport.calcularCoordsViewport(coords)

            # Desenha a linha
            pen = QPen(QColor(self.color), 3)
            painter.setPen(pen)
            painter.drawLine(
                coord_viewport[0][0],
                coord_viewport[0][1],
                coord_viewport[1][0],
                coord_viewport[1][1]
            )
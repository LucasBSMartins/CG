from objects.object import Object
from PySide6.QtGui import QPen, QColor
from utils.setting import Type
from utils.clipping import Clipping

class Wireframe(Object):
    """Classe que representa um objeto gráfico do tipo Wireframe (polígono fechado)"""
    def __init__(self, name, coord, color):
        super().__init__(name, Type.WIREFRAME, coord, color)

    def draw(self, window, painter, viewport, normalized_coords):

        (draw, coords) = Clipping.clip_wireframe_sutherlandHodgeman(normalized_coords, window)

        if draw:
            # Transforma para coordenadas da viewport
            coord_viewport = viewport.calcularCoordsViewport(coords)

            pen = QPen(QColor(self.color), 3)
            painter.setPen(pen)

            # Desenhar as linhas do polígono
            for i, (x, y) in enumerate(coord_viewport):
                if i == len(coord_viewport)-1:
                    painter.drawLine(x, y, coord_viewport[0][0], coord_viewport[0][1])
                else:
                    painter.drawLine(x, y, coord_viewport[i+1][0], coord_viewport[i+1][1])
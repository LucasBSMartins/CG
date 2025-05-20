from objects.object import Object
from utils.setting import Type, ClippingAlgorithm
from PySide6.QtGui import QColor, QPen
from utils.clipping import Clipping

class Object3D(Object):
    def __init__(self, name, coord, color):
        super().__init__(name, Type.OBJECT_3D, coord, color)

    def draw(self, window, painter, viewport, clipping_algorithm, normalized_coords):
        # Criar arestas (linhas) ligando os pontos consecutivos
        edges = [((normalized_coords[i]), (normalized_coords[i + 1])) for i in range(0, len(normalized_coords) - 1, 2)]

        # Desenhar cada uma das arestas como retas 2D normalizadas
        for i in edges:
            line = [i[0], i[1]]

            # Determina se vai desenhar a aresta ou parte da aresta
            if clipping_algorithm == ClippingAlgorithm.COHEN:
                draw, coords = Clipping.clip_line_cohen_sutherland(line, window)
            else:
                draw, coords = Clipping.clip_line_liang_barsky(line, window)

            if draw:
                # Transforma para coordenadas da viewport
                coord_viewport = viewport.calcularCoordsViewport(coords)

                # Desenha a aresta
                pen = QPen(QColor(self.color), 3)
                painter.setPen(pen)
                painter.drawLine(
                    coord_viewport[0][0],
                    coord_viewport[0][1],
                    coord_viewport[1][0],
                    coord_viewport[1][1]
                )
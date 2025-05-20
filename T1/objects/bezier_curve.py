from objects.object import Object
from PySide6.QtGui import QPen, QColor
from utils.setting import Type, ClippingAlgorithm
from utils.clipping import Clipping
from numpy import arange

class BerzierCurve(Object):
    def __init__(self, name, coord, color):
        super().__init__(name, Type.BEZIER_CURVE, coord, color)

    def draw(self, window, painter, viewport, clipping_algorithm, normalized_coords):

        points = self.__get_drawing_points(normalized_coords)

        for i in range(len(points) - 1):
            line = [points[i], points[i + 1]]

            if clipping_algorithm == ClippingAlgorithm.COHEN:
                draw, coords = Clipping.clip_line_cohen_sutherland(line, window)
            else:
                draw, coords = Clipping.clip_line_liang_barsky(line, window)

            if draw:
                coord_viewport = viewport.calcularCoordsViewport(coords)
                pen = QPen(QColor(self.color), 3)
                painter.setPen(pen)
                painter.drawLine(
                    coord_viewport[0][0], coord_viewport[0][1],
                    coord_viewport[1][0], coord_viewport[1][1]
                )

    def __get_drawing_points(self, coords):
        drawing_points = []
        step = 1 / 50

        for i in range(0, len(coords) - 1, 3):
            p1, p2, p3, p4 = coords[i], coords[i + 1], coords[i + 2], coords[i + 3]
            fx = self.__get_blending_function(p1[0], p2[0], p3[0], p4[0])
            fy = self.__get_blending_function(p1[1], p2[1], p3[1], p4[1])

            for t in arange(0, 1.01, step):
                drawing_points.append((fx(t), fy(t)))

        return drawing_points

    def __get_blending_function(self, p1, p2, p3, p4):
        return lambda t: (
            p1 * (-t**3 + 3*t**2 - 3*t + 1) +
            p2 * (3*t**3 - 6*t**2 + 3*t) +
            p3 * (-3*t**3 + 3*t**2) +
            p4 * t**3
        )

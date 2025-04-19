from PySide6.QtWidgets import QLabel
from PySide6.QtGui import QPen, QColor
from PySide6.QtCore import Qt
from utils.setting import Settings
import numpy as np

class Viewport():
    def __init__(self, window):
        self.__window = window

    # Desenhar borda vermelha da viewport
    def drawBorder(self, painter):
        pen = QPen(QColor(255, 0, 0), 4)
        painter.setPen(pen)
        painter.setBrush(Qt.NoBrush)
        painter.drawRect(*Settings.viewport())

    # Normalizar coordenadas
    def normalizeCoords(self, obj_list):
        transforming_matrix = self.__window.windowNormalize()

        # Coordenadas normalizadas de todos objetos da tela
        normalized_coords = []
        for obj in obj_list:
            obj_transformed_coords = []
            for x, y in obj.coord:
                transformed_coord = (np.dot(np.array([x, y, 1]), np.array(transforming_matrix))).tolist()
                obj_transformed_coords.append(transformed_coord[:2])
            normalized_coords.append(obj_transformed_coords)
        return normalized_coords

    # Calcula a coordenada x na viewport a partir da coordenada x na janela de mundo
    def calcularXviewport(self, Xw):
        xw_range = self.__window.xmax_scn - self.__window.xmin_scn
        viewport_range = Settings.viewportXmax() - Settings.viewportXmin()

        normalized_xw = (Xw - self.__window.xmin_scn) / xw_range
        return Settings.viewport()[0] + (normalized_xw * viewport_range)

    # Calcula a coordenada y na viewport a partir da coordenada y na janela de mundo
    def calcularYviewport(self, Yw):
        yw_range = self.__window.ymax_scn - self.__window.ymin_scn
        viewport_range = Settings.viewportYmax() - Settings.viewportYmin()

        normalized_yw = (Yw - self.__window.ymin_scn) / yw_range
        # Inverte o valor de y para corresponder ao sistema de coordenadas da tela
        inverted_normalized_yw = 1 - normalized_yw
        return Settings.viewport()[1] + (inverted_normalized_yw * viewport_range)

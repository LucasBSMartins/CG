from PySide6.QtWidgets import QLabel
from PySide6.QtGui import QPixmap, QPainter
from PySide6.QtCore import Qt
from utils.setting import Settings
import numpy as np

class Viewport(QLabel):
    def __init__(self, parent, window):
        super().__init__(parent)
        self.__window = window
        self.setStyleSheet("border: none;")

        # Define a geometria do viewport com base nas configurações
        self.setGeometry(Settings.viewport()[0],
                        Settings.viewport()[1],
                        Settings.viewport()[2],
                        Settings.viewport()[3])
        # Criação de um QPixmap para armazenar e desenhar os objetos
        self.__pix_map = QPixmap(Settings.viewport()[2], Settings.viewport()[3])
        self.__pix_map.fill(Qt.white)
        self.setPixmap(self.__pix_map)

    def drawViewportObj(self, objts):
        """
        Atualiza o viewport desenhando os objetos na tela.
        """
        self.__pix_map.fill(Qt.white)
        painter = QPainter(self.__pix_map)
        
        # Normalizar as coordenadas
        normalized_coords = self.__normalizeCoords(objts)

        # Desenha todos os objetos de obj_list (e transforma pra Viewport)
        for idx, obj in enumerate(objts):
            coord_viewport = []
            for coord in normalized_coords[idx]:
                x_viewport = self.__calcularXviewport(coord[0])
                y_viewport = self.__calcularYviewport(coord[1])
                coord_viewport.append((x_viewport, y_viewport))
            obj.draw(coord_viewport, painter)
        
        self.setPixmap(self.__pix_map)

    # Normalizar coordenadas
    def __normalizeCoords(self, obj_list):
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

    def __calcularXviewport(self, Xn):
        """
        Converte uma coordenada X normalizada (SCN) para a coordenada correspondente no viewport.
        """
        viewport_variance = Settings.viewportXmax() - Settings.viewportXmin()
        return ((Xn  - (-1))/(1- (-1))) * viewport_variance

    def __calcularYviewport(self, Yn):
        """
        Converte uma coordenada Y normalizada (SCN) para a coordenada correspondente no viewport.
        O eixo Y do viewport é invertido.
        """
        viewport_variance = Settings.viewportYmax() - Settings.viewportYmin()
        return ((1 - ((Yn - (-1))/ (1 - (-1)))) * viewport_variance)

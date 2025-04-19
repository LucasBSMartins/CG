from PySide6.QtWidgets import QLabel
from PySide6.QtGui import QPixmap, QPainter
from PySide6.QtCore import Qt
from utils.setting import Settings
from utils.clipping import Clipping

class Canvas(QLabel):
    def __init__(self, parent, viewport):
        super().__init__(parent)
        self.__viewport = viewport
        self.setStyleSheet("border: none;")
        self.setGeometry(*Settings.canvas())

        # Pixmap para desenhar objetos
        self.__pix_map = QPixmap(Settings.canvas()[2], Settings.canvas()[3])
        self.__pix_map.fill(Qt.white)
        self.setPixmap(self.__pix_map)
    
    def drawObjects(self, obj_list, clipping_algorithm, window):
        """
        Desenha os objetos na viewport após normalização e clipping.

        Args:
            obj_list: Uma lista de objetos a serem desenhados.
            clipping_algorithm: O algoritmo de clipping a ser usado (da enum ClippingAlgorithm).
            window: A instância da classe Window que define a janela de mundo.
        """
        self.__pix_map.fill(Qt.white)
        painter = QPainter(self.__pix_map)

        # Normalizar as coordenadas dos objetos para a janela de mundo normalizada [-1, 1]
        normalized_coords_list = self.__viewport.normalizeCoords(obj_list)

        # Iterar sobre cada objeto para aplicar o clipping e desenhar na viewport
        for idx, obj in enumerate(obj_list):
            normalized_coords = normalized_coords_list[idx]
            draw_clipped, clipped_coords = Clipping.clip(obj, normalized_coords, window, clipping_algorithm)
            
            if draw_clipped:
                viewport_coords = []
                for norm_coord in clipped_coords:
                    x_vp = self.__viewport.calcularXviewport(norm_coord[0])
                    y_vp = self.__viewport.calcularYviewport(norm_coord[1])
                    viewport_coords.append((x_vp, y_vp))
                obj.draw(viewport_coords, painter)

        # Desenhar a borda da viewport
        self.__viewport.drawBorder(painter)

        # Atualizar o QLabel para exibir o desenho
        painter.end()
        self.setPixmap(self.__pix_map)
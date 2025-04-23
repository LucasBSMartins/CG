from PySide6.QtWidgets import QLabel
from PySide6.QtGui import QPixmap, QPainter
from PySide6.QtCore import Qt
from utils.setting import Settings, Type

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
        
        for obj in obj_list:
            if obj.tipo == Type.POINT or obj.tipo == Type.WIREFRAME:
                obj.draw(window, painter, self.__viewport)
            else:
                obj.draw(window, painter, self.__viewport, clipping_algorithm)
        
        self.__viewport.drawBorder(painter)
        
        self.setPixmap(self.__pix_map)
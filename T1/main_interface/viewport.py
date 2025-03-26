from PySide6.QtWidgets import QLabel
from PySide6.QtGui import QPixmap, QPainter
from PySide6.QtCore import Qt
from utils.setting import Settings

class Viewport(QLabel):
    def __init__(self, parent, window):
        super().__init__(parent)
        self.__window = window
        self.setStyleSheet("border: none;")
        self.setGeometry(Settings.viewport()[0],
                        Settings.viewport()[1],
                        Settings.viewport()[2],
                        Settings.viewport()[3])
        # Pixmap para desenhar objetos
        self.__pix_map = QPixmap(Settings.viewport()[2], Settings.viewport()[3])
        self.__pix_map.fill(Qt.white)
        self.setPixmap(self.__pix_map)

    def drawViewportObj(self, objts):
        self.__pix_map.fill(Qt.white)
        painter = QPainter(self.__pix_map)

        for obj in objts:
            coord_viewport = [
                (self.__calcularXviewport(coord[0]), self.__calcularYviewport(coord[1]))
                for coord in obj.coord
            ]
            obj.draw(coord_viewport, painter)

        self.setPixmap(self.__pix_map)

    def __calcularXviewport(self, Xw):
        viewport_variance = Settings.viewportXmax() - Settings.viewportXmin()
        return (((Xw - self.__window.xw_min)/(self.__window.xw_max - self.__window.xw_min)) * viewport_variance)
    
    def __calcularYviewport(self, Yw):
        viewport_variance = Settings.viewportYmax() - Settings.viewportYmin()
        return ((1 - ((Yw - self.__window.yw_min)/ (self.__window.yw_max - self.__window.yw_min))) * viewport_variance)
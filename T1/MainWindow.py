from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QPainter, QColor, QPen
from PyQt5.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("2D Graphics with PyQt5")
        self.setFixedSize(800, 600)
        
        self.center_on_second_monitor()

    def center_on_second_monitor(self):
        """
        Move the window to the center of the second monitor.
        """
        screens = QApplication.screens()  # Get a list of all screens

        if len(screens) > 1:  # Check if there is a second monitor
            second_screen = screens[1]  # Get the second screen
            screen_geometry = second_screen.geometry()  # Get the geometry of the second screen

            # Calculate the center position
            x = screen_geometry.x() + (screen_geometry.width() - self.width()) // 2
            y = screen_geometry.y() + (screen_geometry.height() - self.height()) // 2

            # Move the window to the calculated position
            self.move(x, y)
        else:
            print("No second monitor detected. Window will remain on the primary monitor.")

    def paintEvent(self, event):

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        painter.fillRect(self.rect(), QColor(165, 165, 165)) 

        gap = 20

        viewport_width = self.width() - 220 - gap
        viewport_height = self.height() - 200 
        viewport_x = 220
        viewport_y = gap 
        viewport_rect = (viewport_x, viewport_y, viewport_width, viewport_height)

        painter.fillRect(*viewport_rect, QColor(211, 211, 211))

        painter.setPen(QPen(Qt.black, 2))
        painter.drawRect(*viewport_rect)
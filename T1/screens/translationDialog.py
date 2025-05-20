from PySide6.QtWidgets import QLabel, QSpinBox, QGridLayout, QDialog, QPushButton
from utils.setting import Settings

class TranslationDialog(QDialog):
    def __init__(self, displayFile, objectList, window):
        super().__init__()
        self.__displayFile = displayFile
        self.__objectList = objectList
        self.__window = window
        self.setWindowTitle("Translação")
        self.resize(100, 100)

        self.layout = QGridLayout(self)

        # Inputs para dx e dy
        dx_label = QLabel("Deslocamento eixo x")
        self.__translation_dx = QSpinBox()
        self.__translation_dx.setRange(Settings.min_coord(), Settings.max_coord())
        dy_label = QLabel("Deslocamento eixo y")
        self.__translation_dy = QSpinBox()
        self.__translation_dy.setRange(Settings.min_coord(), Settings.max_coord())
        dz_label = QLabel("Deslocamento eixo z")
        self.__translation_dz = QSpinBox()
        self.__translation_dz.setRange(Settings.min_coord(), Settings.max_coord())

        # Layout
        self.layout.addWidget(dx_label, 0, 0)
        self.layout.addWidget(self.__translation_dx, 0, 1)
        self.layout.addWidget(dy_label, 1, 0)
        self.layout.addWidget(self.__translation_dy, 1, 1)
        self.layout.addWidget(dz_label, 2, 0)
        self.layout.addWidget(self.__translation_dz, 2, 1)

        self.next_button = QPushButton("Avançar")
        self.next_button.clicked.connect(self.next_step)
        self.next_button.setAutoDefault(False)
        self.next_button.setDefault(False)
        self.layout.addWidget(self.next_button, 3, 1)

    def next_step(self):

        self.__selected = self.__objectList.currentRow()
        selected_item = self.__objectList.item(self.__selected)
        selected_item_text = selected_item.text()
        object_name = selected_item_text.split(' (')[0]
        selected_object = self.__displayFile.get_object(object_name)
        selected_object.translate(self.__translation_dx.value(), self.__translation_dy.value(), self.__translation_dz.value())
        self.accept()
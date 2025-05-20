from PySide6.QtWidgets import QLabel, QSpinBox, QGridLayout, QDialog, QPushButton
from utils.setting import Settings

class EscalonamentoDialog(QDialog):
    def __init__(self, displayFile, objectList):
        super().__init__()
        self.__displayFile = displayFile
        self.__objectList = objectList
        self.setWindowTitle("Escalonamento")
        self.resize(100, 100)

        self.layout = QGridLayout(self)

        sx_label = QLabel("Escala no eixo x:")
        self.__input_sx = QSpinBox()
        self.__input_sx.setSingleStep(1)
        self.__input_sx.setValue(1)
        sy_label = QLabel("Escala no eixo y:")
        self.__input_sy = QSpinBox()
        self.__input_sy.setSingleStep(1)
        self.__input_sy.setValue(1)
        sz_label = QLabel("Escala no eixo x:")
        self.__input_sz = QSpinBox()
        self.__input_sz.setSingleStep(1)
        self.__input_sz.setValue(1)
        
        self.layout.addWidget(sx_label, 0, 0)
        self.layout.addWidget(self.__input_sx, 0, 1)
        self.layout.addWidget(sy_label, 1, 0)
        self.layout.addWidget(self.__input_sy, 1, 1)
        self.layout.addWidget(sz_label, 2, 0)
        self.layout.addWidget(self.__input_sz, 2, 1)

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
        selected_object.scale(self.__input_sx.value(), self.__input_sy.value(), self.__input_sz.value())
        self.accept()        
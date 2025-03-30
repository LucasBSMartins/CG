from PySide6.QtWidgets import QLabel, QDoubleSpinBox, QGridLayout, QDialog, QPushButton
from tools.objectTransformator import ObjectTransformator

class EscalonamentoDialog(QDialog):
    def __init__(self, displayFile, objectList):
        super().__init__()
        self.__displayFile = displayFile
        self.__objectList = objectList
        self.setWindowTitle("Escalonamento")
        self.resize(100, 100)

        self.layout = QGridLayout(self)

        # Input para escala
        scale_label = QLabel("Valor da escala:")
        self.__scale_input = QDoubleSpinBox()
        self.__scale_input.setRange(-100, 100)
        self.__scale_input.setSingleStep(0.1)
        
        # Layout
        self.layout.addWidget(scale_label, 0, 0)
        self.layout.addWidget(self.__scale_input, 0, 1)
        
        self.next_button = QPushButton("Avançar")
        self.next_button.clicked.connect(self.next_step)
        self.next_button.setAutoDefault(False)
        self.next_button.setDefault(False)
        self.layout.addWidget(self.next_button, 1, 1)

    def next_step(self):
        ObjectTransformator()
        self.accept()
        
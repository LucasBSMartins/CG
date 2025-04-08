from PySide6 import QtWidgets

from screens.translationDialog import TranslationDialog
from screens.escalonamentoDialog import EscalonamentoDialog
from screens.rotationDialog import RotationDialog

class TransformObjectDialog(QtWidgets.QDialog):
    """Janela inicial para escolher o tipo de objeto."""
    def __init__(self, displayFile, objectList, window):
        super().__init__()
        self.__displayFile = displayFile
        self.__objectList = objectList
        self.__window = window
        self.setWindowTitle("Transformações")
        self.resize(100, 100)

        self.layout = QtWidgets.QVBoxLayout(self)
        self.combo_box = QtWidgets.QComboBox(self)
        self.combo_box.addItems(["Translação", "Escalonamento", "Rotação"])

        self.layout.addWidget(QtWidgets.QLabel("Escolha o tipo de transformação:"))
        self.layout.addWidget(self.combo_box)
       
        self.next_button = QtWidgets.QPushButton("Avançar")
        self.next_button.clicked.connect(self.next_step)
        self.next_button.setAutoDefault(False)
        self.next_button.setDefault(False)
        self.layout.addWidget(self.next_button)

        self.selected_object = None

    def next_step(self):
        """Abre a tela de inserção de pontos ao selecionar um objeto."""
        self.selected_object = self.combo_box.currentText()
        self.accept()

        if self.selected_object == "Translação":
            self.__translationDialog = TranslationDialog(self.__displayFile, self.__objectList, self.__window)
            self.__translationDialog.exec()

        elif self.selected_object == "Escalonamento":
            self.__escalonamentoDialog = EscalonamentoDialog(self.__displayFile, self.__objectList)
            self.__escalonamentoDialog.exec()

        elif self.selected_object == "Rotação":
            self.__rotacaoDialog = RotationDialog(self.__displayFile, self.__objectList)
            self.__rotacaoDialog.exec()
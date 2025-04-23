from PySide6 import QtWidgets

from screens.addObjectDialog import AddObjectDialog

class ObjectSelectionDialog(QtWidgets.QDialog):
    """Janela inicial para escolher o tipo de objeto."""
    def __init__(self, displayFile, objectList):
        super().__init__()
        self.__displayFile = displayFile
        self.__objectList = objectList
        self.setWindowTitle("Escolher Objeto")
        self.resize(100, 100)

        self.layout = QtWidgets.QVBoxLayout(self)
        self.combo_box = QtWidgets.QComboBox(self)
        self.combo_box.addItems(["Ponto", "Reta", "Polígono", "Curva de Bézier"])

        self.layout.addWidget(QtWidgets.QLabel("Escolha o tipo de objeto:"))
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
        addObject = AddObjectDialog(self.selected_object, self.__displayFile, self.__objectList)
        addObject.exec()
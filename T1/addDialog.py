from PySide6 import QtWidgets
from PySide6.QtWidgets import QMessageBox, QLabel, QLineEdit
from addPoint import AddPoint
from addLine import AddLine
from addWireframe import AddWireframe

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
        self.combo_box.addItems(["Ponto", "Reta", "Polígono"])

        self.layout.addWidget(QtWidgets.QLabel("Escolha o tipo de objeto:"))
        self.layout.addWidget(self.combo_box)
       
        self.next_button = QtWidgets.QPushButton("Avançar")
        self.next_button.clicked.connect(self.next_step)
        self.layout.addWidget(self.next_button)

        self.selected_object = None

    def next_step(self):
        """Abre a tela de inserção de pontos ao selecionar um objeto."""
        self.selected_object = self.combo_box.currentText()
        self.accept()        
        addObject = AddObjectDialog(self.selected_object, self.__displayFile, self.__objectList)
        addObject.exec()

class AddObjectDialog(QtWidgets.QDialog):
    """Janela para inserir coordenadas do objeto escolhido."""
    def __init__(self, selected_object, displayFile, objectList):
        super().__init__()
        self.setWindowTitle("Adicionar Objeto")
        self.resize(300, 400)
        self.__displayFile = displayFile
        self.__objectList = objectList
       
        self.selected_object = selected_object
        self.layout = QtWidgets.QVBoxLayout(self)

        name_layout = QtWidgets.QHBoxLayout()  # Layout para o nome
        self.__name_label = QLabel("Nome:")
        self.__name_input = QLineEdit()
        name_layout.addWidget(self.__name_label)
        name_layout.addWidget(self.__name_input)
        self.layout.addLayout(name_layout)
                              
        self.scroll_area = QtWidgets.QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_widget = QtWidgets.QWidget()
        self.scroll_layout = QtWidgets.QVBoxLayout(self.scroll_widget)
        self.scroll_area.setWidget(self.scroll_widget)

        self.layout.addWidget(QtWidgets.QLabel(f"Inserir coordenadas para {selected_object}:"))
        self.layout.addWidget(self.scroll_area)

        self.add_fields()

        self.add_button = QtWidgets.QPushButton("Adicionar")
        self.add_button.clicked.connect(self.add_object)
        self.layout.addWidget(self.add_button)

    def add_fields(self):
        """Gera dinamicamente os campos de entrada conforme o tipo de objeto."""
        if self.selected_object == "Ponto":
            self.scroll_layout.addWidget(QtWidgets.QLabel("Coordenadas (X, Y):"))
            self.x_input = QtWidgets.QLineEdit(self)
            self.y_input = QtWidgets.QLineEdit(self)
            self.scroll_layout.addWidget(self.x_input)
            self.scroll_layout.addWidget(self.y_input)

        elif self.selected_object == "Reta":
            self.scroll_layout.addWidget(QtWidgets.QLabel("Ponto 1 (X1, Y1):"))
            self.x1_input = QtWidgets.QLineEdit(self)
            self.y1_input = QtWidgets.QLineEdit(self)
            self.scroll_layout.addWidget(self.x1_input)
            self.scroll_layout.addWidget(self.y1_input)

            self.scroll_layout.addWidget(QtWidgets.QLabel("Ponto 2 (X2, Y2):"))
            self.x2_input = QtWidgets.QLineEdit(self)
            self.y2_input = QtWidgets.QLineEdit(self)
            self.scroll_layout.addWidget(self.x2_input)
            self.scroll_layout.addWidget(self.y2_input)

        elif self.selected_object == "Polígono":
            self.scroll_layout.addWidget(QtWidgets.QLabel("Número de pontos:"))
            self.qtd_input = QtWidgets.QSpinBox(self)
            self.qtd_input.setMinimum(3)
            self.qtd_input.setValue(3)
            self.qtd_input.valueChanged.connect(self.generate_polygon_fields)
            self.scroll_layout.addWidget(self.qtd_input)

            self.points_container = QtWidgets.QVBoxLayout()
            self.scroll_layout.addLayout(self.points_container)
            self.generate_polygon_fields()

    def generate_polygon_fields(self):
        """Gera dinamicamente os campos de coordenadas para o polígono."""
        for i in reversed(range(self.points_container.count())):
            widget = self.points_container.itemAt(i).widget()
            if widget:
                widget.deleteLater()

        self.point_inputs = []
        qtd_pontos = self.qtd_input.value()

        for i in range(qtd_pontos):
            label = QtWidgets.QLabel(f"Ponto {i+1} (X, Y):")
            x_input = QtWidgets.QLineEdit(self)
            y_input = QtWidgets.QLineEdit(self)
            self.points_container.addWidget(label)
            self.points_container.addWidget(x_input)
            self.points_container.addWidget(y_input)
            self.point_inputs.append((x_input, y_input))

        self.scroll_widget.setLayout(self.scroll_layout)

    def add_object(self):

        nome = self.__name_input.text().strip()
        if not nome:
            self.noName() 
            return

        if (self.__objectList):
            if nome in self.__displayFile.get_names():  
                self.repeatedName()  
                return
        
        def is_valid_number(value):
            try:
                int(value)
                return True
            except ValueError:
                return False
        
        if self.selected_object == "Ponto":
            x = self.x_input.text().strip()
            y = self.y_input.text().strip()
            if not x or not y:
                self.noPoints()
                return
            if not is_valid_number(x) or not is_valid_number(y):
                self.noPoints()  
                return
            x, y = int(x), int(y)
            addpoint = AddPoint()
            point = addpoint.create(nome, [(x, y)])
            self.__displayFile.addObject(point)           
            
        elif self.selected_object == "Reta":
            x1 = self.x1_input.text().strip()
            y1 = self.y1_input.text().strip()
            x2 = self.x2_input.text().strip()
            y2 = self.y2_input.text().strip()
            if not x1 or not y1 or not x2 or not y2:
                self.noPoints()
                return
            if not (is_valid_number(x1) and is_valid_number(y1) and is_valid_number(x2) and is_valid_number(y2)):
                self.noPoints()  
                return
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            addLine = AddLine()
            line = addLine.create(nome, [(x1, y1), (x2, y2)])
            self.__displayFile.addObject(line)
            
        elif self.selected_object == "Polígono":
            qtd = self.qtd_input.value()
            pontos = [(x.text().strip(), y.text().strip()) for x, y in self.point_inputs]
            if any(not x or not y for x, y in pontos):
                self.noPoints()
                return
            if any(not is_valid_number(x) or not is_valid_number(y) for x, y in pontos):
                self.noPoints()  
                return
            pontos = [(int(x.text().strip()), int(y.text().strip())) for x, y in self.point_inputs]

            addWireframe = AddWireframe(qtd)
            wireframe = addWireframe.create(nome, pontos)
            self.__displayFile.addObject(wireframe)
        
        self.__objectList.addItem(str(nome) + " (" + self.selected_object + ")")  
            
        print(self.__displayFile.objects_list) 
        self.accept()

    def noName(self):
        """Exibe mensagem de aviso para nome vazio."""
        message = QMessageBox()
        message.setWindowTitle("Aviso")
        message.setText("Dê um nome ao objeto")
        message.setIcon(QMessageBox.Warning)
        message.setStyleSheet("background-color: rgb(212,208,200); color: black;")
        message.setFixedSize(400, 200)
        message.exec()

    def repeatedName(self):
        """Exibe mensagem de aviso para nome repetido."""
        message = QMessageBox()
        message.setWindowTitle("Aviso")
        message.setText("Esse nome já existe")
        message.setIcon(QMessageBox.Warning)
        message.setStyleSheet("background-color: rgb(212,208,200); color: black;")
        message.setFixedSize(400, 200)
        message.exec()

    def noPoints(self):
        """Exibe mensagem de aviso quando os pontos não foram preenchidos."""
        message = QMessageBox()
        message.setWindowTitle("Aviso")
        message.setIcon(QMessageBox.Warning)
        message.setText("Por favor, preencha todas as coordenadas.")
        message.setStyleSheet("background-color: rgb(212,208,200); color: black;")
        message.setFixedSize(400, 200)
        message.exec()

from PySide6 import QtWidgets

from PySide6.QtWidgets import QLabel, QLineEdit
from utils.wnr import Wnr
from tools.addPoint import AddPoint
from tools.addLine import AddLine
from screens.colorPickerWidget import ColorPickerWidget
from tools.addWireframe import AddWireframe

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

        name_layout = QtWidgets.QHBoxLayout()
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
        self.color_picker = ColorPickerWidget()
        self.layout.addWidget(self.color_picker)

        self.add_button = QtWidgets.QPushButton("Adicionar")
        self.add_button.clicked.connect(self.add_object)
        self.layout.addWidget(self.add_button)
        self.add_button.setAutoDefault(False)
        self.add_button.setDefault(False)

    def add_fields(self):
        """Gera dinamicamente os campos de entrada conforme o tipo de objeto."""
        if self.selected_object == "Ponto":
            self.scroll_layout.addWidget(QtWidgets.QLabel("Coordenadas (X, Y):"))
            self.x_input = QtWidgets.QLineEdit(self)
            self.y_input = QtWidgets.QLineEdit(self)
            self.x_input.setText("0")
            self.y_input.setText("0")
            self.scroll_layout.addWidget(self.x_input)
            self.scroll_layout.addWidget(self.y_input)

        elif self.selected_object == "Reta":
            self.scroll_layout.addWidget(QtWidgets.QLabel("Ponto 1 (X1, Y1):"))
            self.x1_input = QtWidgets.QLineEdit(self)
            self.y1_input = QtWidgets.QLineEdit(self)
            self.x1_input.setText("0")
            self.y1_input.setText("0")
            self.scroll_layout.addWidget(self.x1_input)
            self.scroll_layout.addWidget(self.y1_input)

            self.scroll_layout.addWidget(QtWidgets.QLabel("Ponto 2 (X2, Y2):"))
            self.x2_input = QtWidgets.QLineEdit(self)
            self.y2_input = QtWidgets.QLineEdit(self)
            self.x2_input.setText("0")
            self.y2_input.setText("0")
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
            x_input.setText("0")
            y_input.setText("0")
            self.points_container.addWidget(label)
            self.points_container.addWidget(x_input)
            self.points_container.addWidget(y_input)
            self.point_inputs.append((x_input, y_input))

        self.scroll_widget.setLayout(self.scroll_layout)

    def add_object(self):

        nome = self.__name_input.text().strip()
        if not nome:
            Wnr.noName()
            return

        if (self.__objectList):
            if nome in self.__displayFile.get_names():  
                Wnr.repeatedName() 
                return
        
        def is_valid_number(value):
            try:
                int(value)
                return True
            except ValueError:
                return False

        selected_color = self.color_picker.get_selected_color()
       
        if self.selected_object == "Ponto":
            x = self.x_input.text().strip()
            y = self.y_input.text().strip()
            if not x or not y:
                Wnr.noPoints()
                return
            if not is_valid_number(x) or not is_valid_number(y):
                Wnr.invalidValor() 
                return
            x, y = int(x), int(y)
            addpoint = AddPoint()
            point = addpoint.create(nome, [(x, y)], selected_color)
            self.__displayFile.addObject(point)           
            
        elif self.selected_object == "Reta":
            x1 = self.x1_input.text().strip()
            y1 = self.y1_input.text().strip()
            x2 = self.x2_input.text().strip()
            y2 = self.y2_input.text().strip()
            if not x1 or not y1 or not x2 or not y2:
                Wnr.noPoints()
                return
            if not (is_valid_number(x1) and is_valid_number(y1) and is_valid_number(x2) and is_valid_number(y2)):
                Wnr.invalidValor()  
                return
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            addLine = AddLine()
            line = addLine.create(nome, [(x1, y1), (x2, y2)], selected_color)
            self.__displayFile.addObject(line)
            
        elif self.selected_object == "Polígono":
            qtd = self.qtd_input.value()
            pontos = [(x.text().strip(), y.text().strip()) for x, y in self.point_inputs]
            if any(not x or not y for x, y in pontos):
                Wnr.noPoints()
                return
            if any(not is_valid_number(x) or not is_valid_number(y) for x, y in pontos):
                Wnr.invalidValor()  
                return
            pontos = [(int(x.text().strip()), int(y.text().strip())) for x, y in self.point_inputs]

            addWireframe = AddWireframe(qtd)
            wireframe = addWireframe.create(nome, pontos, selected_color)
            self.__displayFile.addObject(wireframe)
        
        self.__objectList.addItem(str(nome) + " (" + self.selected_object + ")")  
            
        self.accept()

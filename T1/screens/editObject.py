from PySide6 import QtWidgets
from PySide6.QtWidgets import QLabel, QLineEdit, QDoubleSpinBox
from objects.point import Point
from objects.line import Line
from utils.wnr import Wnr
from objects.wireframe import Wireframe
from screens.colorPickerWidget import ColorPickerWidget


class EditObject(QtWidgets.QDialog):
    """Janela para editar as coordenadas do objeto escolhido."""
    def __init__(self, selected_object, displayFile, objectList):
        super().__init__()
        self.setWindowTitle(f"Editar {selected_object.name}")
        self.resize(300, 400)
        self.__displayFile = displayFile
        self.__objectList = objectList
        self.selected_object = selected_object

        self.object_to_edit = self.selected_object

        self.layout = QtWidgets.QVBoxLayout(self)

        name_layout = QtWidgets.QHBoxLayout()
        self.__name_label = QLabel("Nome:")
        self.__name_input = QLineEdit()
        self.__name_input.setText(self.object_to_edit.name)
        name_layout.addWidget(self.__name_label)
        name_layout.addWidget(self.__name_input)
        self.layout.addLayout(name_layout)

        self.scroll_area = QtWidgets.QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_widget = QtWidgets.QWidget()
        self.scroll_layout = QtWidgets.QVBoxLayout(self.scroll_widget)
        self.scroll_area.setWidget(self.scroll_widget)

        self.layout.addWidget(QtWidgets.QLabel(f"Editar coordenadas para {selected_object.name}:"))
        self.layout.addWidget(self.scroll_area)

        self.add_fields()
        self.color_picker = ColorPickerWidget()
        self.layout.addWidget(self.color_picker)

        self.add_button = QtWidgets.QPushButton("Salvar")
        self.add_button.clicked.connect(self.save_object)
        self.layout.addWidget(self.add_button)

    def add_fields(self):
        if isinstance(self.selected_object, Point):
            self.scroll_layout.addWidget(QtWidgets.QLabel("Coordenadas (X, Y):"))
            
            self.x_input = QDoubleSpinBox(self)
            self.y_input = QDoubleSpinBox(self)
            
            self.x_input.setDecimals(0)  
            self.y_input.setDecimals(0)
            self.x_input.setMaximum(1000000000)
            self.y_input.setMaximum(1000000000)
            
            x_coord, y_coord = self.object_to_edit.coord[0] 
            self.x_input.setValue(x_coord)
            self.y_input.setValue(y_coord)

            self.scroll_layout.addWidget(self.x_input)
            self.scroll_layout.addWidget(self.y_input)

        elif isinstance(self.selected_object, Line):
            self.scroll_layout.addWidget(QtWidgets.QLabel("Ponto 1 (X1, Y1):"))
            self.x1_input = QDoubleSpinBox(self)
            self.y1_input = QDoubleSpinBox(self)
            
            self.x1_input.setDecimals(0)
            self.y1_input.setDecimals(0)
            self.x1_input.setMaximum(1000000000)
            self.y1_input.setMaximum(1000000000)
            
            x1_coord, y1_coord = self.object_to_edit.coord[0]  
            self.x1_input.setValue(x1_coord)
            self.y1_input.setValue(y1_coord)
            
            self.scroll_layout.addWidget(self.x1_input)
            self.scroll_layout.addWidget(self.y1_input)

            self.scroll_layout.addWidget(QtWidgets.QLabel("Ponto 2 (X2, Y2):"))
            self.x2_input = QDoubleSpinBox(self)
            self.y2_input = QDoubleSpinBox(self)
            
            self.x2_input.setDecimals(0)
            self.y2_input.setDecimals(0)
            self.x2_input.setMaximum(1000000000)
            self.y2_input.setMaximum(1000000000)

            x2_coord, y2_coord = self.object_to_edit.coord[1]
            self.x2_input.setValue(x2_coord)
            self.y2_input.setValue(y2_coord)

            self.scroll_layout.addWidget(self.x2_input)
            self.scroll_layout.addWidget(self.y2_input)

        elif isinstance(self.selected_object, Wireframe):
            self.scroll_layout.addWidget(QtWidgets.QLabel("Número de pontos:"))
            self.qtd_input = QtWidgets.QSpinBox(self)
            self.qtd_input.setMinimum(3)
            self.qtd_input.setValue(len(self.object_to_edit.coord))
            self.qtd_input.valueChanged.connect(self.generate_polygon_fields)
            self.scroll_layout.addWidget(self.qtd_input)

            self.points_container = QtWidgets.QVBoxLayout()
            self.scroll_layout.addLayout(self.points_container)
            self.generate_polygon_fields()

    def generate_polygon_fields(self):
        for i in reversed(range(self.points_container.count())):
            widget = self.points_container.itemAt(i).widget()
            if widget:
                widget.deleteLater()

        self.point_inputs = []
        qtd_pontos = self.qtd_input.value()

        for i in range(qtd_pontos):
            label = QtWidgets.QLabel(f"Ponto {i+1} (X, Y):")
            x_input = QtWidgets.QDoubleSpinBox(self)
            y_input = QtWidgets.QDoubleSpinBox(self)

            x_input.setDecimals(0)  
            y_input.setDecimals(0)  
            
            x_input.setMaximum(1000000000)  
            y_input.setMaximum(1000000000)

            self.point_inputs.append((x_input, y_input))
            self.points_container.addWidget(label)
            self.points_container.addWidget(x_input)
            self.points_container.addWidget(y_input)
            
            if i < len(self.object_to_edit.coord):
                x_input.setValue(self.object_to_edit.coord[i][0]) 
                y_input.setValue(self.object_to_edit.coord[i][1])

        self.scroll_widget.setLayout(self.scroll_layout)

    def save_object(self):
        
        nome = self.__name_input.text().strip()
        if not nome:
            Wnr.noName()
            return

        if (self.__objectList):
            if nome in self.__displayFile.get_names() and nome != self.object_to_edit.name:  
                Wnr.repeatedName()
                return

        def is_valid_number(value):
            try:
                int(value)
                return True
            except ValueError:
                return False
        
        selected_color = self.color_picker.get_selected_color()

        if isinstance(self.selected_object, Point):
            x = self.x_input.text().strip()
            y = self.y_input.text().strip()
            if not x or not y:
                Wnr.noPoints()
                return
            if not is_valid_number(x) or not is_valid_number(y):
                Wnr.noPoints()  
                return
            x, y = int(x), int(y)
            self.object_to_edit.coord = [(x, y)]
            self.object_to_edit.name = str(nome) 
            self.object_to_edit.color = selected_color
            
            
        elif isinstance(self.selected_object, Line):
            x1 = self.x1_input.text().strip()
            y1 = self.y1_input.text().strip()
            x2 = self.x2_input.text().strip()
            y2 = self.y2_input.text().strip()
            if not x1 or not y1 or not x2 or not y2:
                Wnr.noPoints()
                return
            if not (is_valid_number(x1) and is_valid_number(y1) and is_valid_number(x2) and is_valid_number(y2)):
                Wnr.noPoints()  
                return
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            self.object_to_edit.coord = [(x1, y1), (x2, y2)] 
            self.object_to_edit.name = str(nome) 
            self.object_to_edit.color = selected_color


        elif isinstance(self.selected_object, Wireframe):
            pontos = [(x.text().strip(), y.text().strip()) for x, y in self.point_inputs]
            if any(not x or not y for x, y in pontos):
                Wnr.noPoints()
                return
            if any(not is_valid_number(x) or not is_valid_number(y) for x, y in pontos):
                Wnr.noPoints()  
                return
            pontos = [(int(x.text().strip()), int(y.text().strip())) for x, y in self.point_inputs]

            self.object_to_edit.coord = pontos
            self.object_to_edit.name = str(nome)
            self.object_to_edit.color = selected_color
        self.object_type = ""
        if isinstance(self.object_to_edit, Point):
            self.object_type = " (Ponto)"
        elif isinstance(self.object_to_edit, Line):
            self.object_type = " (Reta)"
        elif isinstance(self.object_to_edit, Wireframe):
            self.object_type = " (Polígono)"

        
        self.accept()
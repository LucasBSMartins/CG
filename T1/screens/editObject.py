from PySide6 import QtWidgets
from PySide6.QtWidgets import QLabel, QLineEdit, QDoubleSpinBox, QSpinBox
from objects.point import Point
from objects.line import Line
from objects.wireframe import Wireframe
from objects.bezier_curve import BerzierCurve
from utils.wnr import Wnr
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

        self.main_layout = QtWidgets.QVBoxLayout(self)
        self._create_name_input()
        self._create_scrollable_area()
        self._create_coordinate_inputs()
        self._create_color_picker()
        self._create_action_buttons()

    def _create_name_input(self):
        """Cria o campo de entrada para o nome do objeto."""
        name_layout = QtWidgets.QHBoxLayout()
        self.__name_label = QLabel("Nome:")
        self.__name_input = QLineEdit()
        self.__name_input.setText(self.object_to_edit.name)
        name_layout.addWidget(self.__name_label)
        name_layout.addWidget(self.__name_input)
        self.main_layout.addLayout(name_layout)

    def _create_scrollable_area(self):
        """Cria a área scrollable para conter os campos de entrada de coordenadas."""
        self.scroll_area = QtWidgets.QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_widget = QtWidgets.QWidget()
        self.scroll_layout = QtWidgets.QVBoxLayout(self.scroll_widget)
        self.scroll_area.setWidget(self.scroll_widget)
        self.main_layout.addWidget(QtWidgets.QLabel(f"Editar coordenadas para {self.selected_object.name}:"))
        self.main_layout.addWidget(self.scroll_area)

    def _create_coordinate_inputs(self):
        """Cria os campos de entrada de coordenadas com base no tipo do objeto."""
        if isinstance(self.selected_object, Point):
            self._create_point_inputs()
        elif isinstance(self.selected_object, Line):
            self._create_line_inputs()
        elif isinstance(self.selected_object, Wireframe):
            self._create_wireframe_inputs()
        elif isinstance(self.selected_object, BerzierCurve):
            self._create_bezier_inputs()
        self.scroll_widget.setLayout(self.scroll_layout)

    def _create_point_inputs(self):
        """Cria os campos de entrada para um ponto (X, Y)."""
        self.scroll_layout.addWidget(QLabel("Coordenadas (X, Y):"))
        self.x_input = self._create_coordinate_spinbox(self.object_to_edit.coord[0][0])
        self.y_input = self._create_coordinate_spinbox(self.object_to_edit.coord[0][1])
        self.scroll_layout.addWidget(self.x_input)
        self.scroll_layout.addWidget(self.y_input)

    def _create_line_inputs(self):
        """Cria os campos de entrada para uma linha (X1, Y1, X2, Y2)."""
        self.scroll_layout.addWidget(QLabel("Ponto 1 (X1, Y1):"))
        self.x1_input = self._create_coordinate_spinbox(self.object_to_edit.coord[0][0])
        self.y1_input = self._create_coordinate_spinbox(self.object_to_edit.coord[0][1])
        self.scroll_layout.addWidget(self.x1_input)
        self.scroll_layout.addWidget(self.y1_input)

        self.scroll_layout.addWidget(QLabel("Ponto 2 (X2, Y2):"))
        self.x2_input = self._create_coordinate_spinbox(self.object_to_edit.coord[1][0])
        self.y2_input = self._create_coordinate_spinbox(self.object_to_edit.coord[1][1])
        self.scroll_layout.addWidget(self.x2_input)
        self.scroll_layout.addWidget(self.y2_input)

    def _create_wireframe_inputs(self):
        """Cria os campos de entrada para um wireframe (polígono)."""
        self.scroll_layout.addWidget(QLabel("Número de pontos:"))
        self.qtd_input = QSpinBox(self)
        self.qtd_input.setMinimum(3)
        self.qtd_input.setMaximum(100)
        self.qtd_input.setValue(len(self.object_to_edit.coord))
        self.qtd_input.valueChanged.connect(self._generate_polygon_fields)
        self.scroll_layout.addWidget(self.qtd_input)

        self.points_container = QtWidgets.QVBoxLayout()
        self.scroll_layout.addLayout(self.points_container)
        self._generate_polygon_fields()

    def _generate_polygon_fields(self):
        """Gera dinamicamente os campos de entrada para os pontos do polígono."""
        self._clear_layout(self.points_container)
        self.point_inputs = []
        qtd_pontos = self.qtd_input.value()

        for i in range(qtd_pontos):
            label = QLabel(f"Ponto {i + 1} (X, Y):")
            x_input = self._create_coordinate_spinbox(self.object_to_edit.coord[i][0] if i < len(self.object_to_edit.coord) else 0)
            y_input = self._create_coordinate_spinbox(self.object_to_edit.coord[i][1] if i < len(self.object_to_edit.coord) else 0)
            self.point_inputs.append((x_input, y_input))
            self.points_container.addWidget(label)
            self.points_container.addWidget(x_input)
            self.points_container.addWidget(y_input)
        self.scroll_widget.setLayout(self.scroll_layout)

    def _create_bezier_inputs(self):
        """Cria os campos de entrada para a curva de Bézier."""
        self.scroll_layout.addWidget(QLabel("Número de pontos de controle:"))
        self.num_control_points_input = QSpinBox(self)
        self.num_control_points_input.setMinimum(2)  # Bézier precisa de pelo menos 2 pontos
        self.num_control_points_input.setMaximum(100) # Define um limite máximo razoável
        self.num_control_points_input.setValue(len(self.object_to_edit.coord))
        self.num_control_points_input.valueChanged.connect(self._generate_bezier_fields)
        self.scroll_layout.addWidget(self.num_control_points_input)

        self.control_points_container = QtWidgets.QVBoxLayout()
        self.scroll_layout.addLayout(self.control_points_container)
        self._generate_bezier_fields()

    def _generate_bezier_fields(self):
        """Gera dinamicamente os campos de entrada para os pontos de controle da Bézier."""
        self._clear_layout(self.control_points_container)
        self.control_point_inputs = []
        num_control_points = self.num_control_points_input.value()

        for i in range(num_control_points):
            label = QLabel(f"Ponto de Controle {i + 1} (X, Y):")
            x_input = self._create_coordinate_spinbox(self.object_to_edit.coord[i][0] if i < len(self.object_to_edit.coord) else 0)
            y_input = self._create_coordinate_spinbox(self.object_to_edit.coord[i][1] if i < len(self.object_to_edit.coord) else 0)
            self.control_point_inputs.append((x_input, y_input))
            self.control_points_container.addWidget(label)
            self.control_points_container.addWidget(x_input)
            self.control_points_container.addWidget(y_input)
        self.scroll_widget.setLayout(self.scroll_layout)

    def _create_coordinate_spinbox(self, value=0.0):
        """Cria um QDoubleSpinBox para entrada de coordenadas com configurações consistentes."""
        spinbox = QDoubleSpinBox(self)
        spinbox.setDecimals(0)
        spinbox.setMaximum(1000000000)
        spinbox.setMinimum(-1000000000)
        spinbox.setValue(value)
        return spinbox

    def _clear_layout(self, layout):
        """Limpa todos os widgets de um layout."""
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

    def _create_color_picker(self):
        """Cria o widget de seleção de cor."""
        self.color_picker = ColorPickerWidget(initial_color=self.selected_object.color)
        # Passa 'self' como o widget pai
        self.main_layout.addWidget(self.color_picker)

    def _create_action_buttons(self):
        """Cria os botões de ação (Salvar)."""
        self.add_button = QtWidgets.QPushButton("Salvar")
        self.add_button.clicked.connect(self.save_object)
        self.main_layout.addWidget(self.add_button)

    def save_object(self):
        """Salva as alterações feitas no objeto."""
        nome = self.__name_input.text().strip()
        if not nome:
            Wnr.noName()
            return

        if self.__objectList and nome in self.__displayFile.get_names() and nome != self.object_to_edit.name:
            Wnr.repeatedName()
            return

        selected_color = self.color_picker.get_selected_color()

        if isinstance(self.selected_object, Point):
            x_str = self.x_input.text().strip()
            y_str = self.y_input.text().strip()
            if not x_str or not y_str or not self._is_valid_number(x_str) or not self._is_valid_number(y_str):
                Wnr.noPoints()
                return
            x, y = int(x_str), int(y_str)
            self.object_to_edit.coord = [(x, y)]
            self.object_type = " (Ponto)"  # Define object_type aqui
        elif isinstance(self.selected_object, Line):
            x1_str = self.x1_input.text().strip()
            y1_str = self.y1_input.text().strip()
            x2_str = self.x2_input.text().strip()
            y2_str = self.y2_input.text().strip()
            if not all([x1_str, y1_str, x2_str, y2_str]) or not all(self._is_valid_number(s) for s in [x1_str, y1_str, x2_str, y2_str]):
                Wnr.noPoints()
                return
            x1, y1, x2, y2 = map(int, [x1_str, y1_str, x2_str, y2_str])
            self.object_to_edit.coord = [(x1, y1), (x2, y2)]
            self.object_type = " (Reta)"  # Define object_type aqui
        elif isinstance(self.selected_object, Wireframe):
            pontos_str = [(x.text().strip(), y.text().strip()) for x, y in self.point_inputs]
            if any(not px or not py for px, py in pontos_str) or any(not self._is_valid_number(p) for px, py in pontos_str for p in (px, py)):
                Wnr.noPoints()
                return
            self.object_to_edit.coord = [(int(px), int(py)) for px, py in pontos_str]
            self.object_type = " (Polígono)"  # Define object_type aqui
        elif isinstance(self.selected_object, BerzierCurve):
            control_points_str = [(x.text().strip(), y.text().strip()) for x, y in self.control_point_inputs]
            if any(not px or not py for px, py in control_points_str) or any(not self._is_valid_number(p) for px, py in control_points_str for p in (px, py)):
                Wnr.noPoints()
                return
            self.object_to_edit.coord = [(int(px), int(py)) for px, py in control_points_str]
            self.object_type = " (Curva de Bézier)" # Define object_type aqui

        self.object_to_edit.name = str(nome)
        self.object_to_edit.color = selected_color
        self.accept()

    def _is_valid_number(self, value_str):
        """Verifica se uma string representa um número inteiro válido."""
        try:
            int(value_str)
            return True
        except ValueError:
            return False
from PySide6 import QtWidgets
from PySide6.QtWidgets import QLabel, QDoubleSpinBox, QSpinBox
from utils.wnr import Wnr


class CoordinateSpinboxCreator:
    @staticmethod
    def create_spinbox(parent, value=0.0):
        """Cria um QDoubleSpinBox para entrada de coordenadas com configurações consistentes."""
        spinbox = QDoubleSpinBox(parent)
        spinbox.setDecimals(0)
        spinbox.setMaximum(1000000000)
        spinbox.setMinimum(-1000000000)
        spinbox.setValue(value)
        return spinbox


class EditObjectInputs:
    def __init__(self, parent):
        self.parent = parent

    def _create_point_inputs(self, point):
        """Cria os campos de entrada para um ponto (X, Y, Z)."""
        self.parent.scroll_layout.addWidget(QLabel("Coordenadas (X, Y, Z):"))

        self.x_input = self._create_coordinate_spinbox(point.coord[0][0])
        self.y_input = self._create_coordinate_spinbox(point.coord[0][1])
        self.z_input = self._create_coordinate_spinbox(point.coord[0][2])

        self.parent.scroll_layout.addWidget(self.x_input)
        self.parent.scroll_layout.addWidget(self.y_input)
        self.parent.scroll_layout.addWidget(self.z_input)

    def _create_line_inputs(self, line):
        """Cria os campos de entrada para uma linha (X1, Y1, Z1, X2, Y2, Z2)."""

        self.parent.scroll_layout.addWidget(QLabel("Ponto 1 (X1, Y1, Z1):"))
        self.x1_input = self._create_coordinate_spinbox(line.coord[0][0])
        self.y1_input = self._create_coordinate_spinbox(line.coord[0][1])
        self.z1_input = self._create_coordinate_spinbox(line.coord[0][2])
        self.parent.scroll_layout.addWidget(self.x1_input)
        self.parent.scroll_layout.addWidget(self.y1_input)
        self.parent.scroll_layout.addWidget(self.z1_input)

        self.parent.scroll_layout.addWidget(QLabel("Ponto 2 (X2, Y2, Z2):"))
        self.x2_input = self._create_coordinate_spinbox(line.coord[1][0])
        self.y2_input = self._create_coordinate_spinbox(line.coord[1][1])
        self.z2_input = self._create_coordinate_spinbox(line.coord[1][2])
        self.parent.scroll_layout.addWidget(self.x2_input)
        self.parent.scroll_layout.addWidget(self.y2_input)
        self.parent.scroll_layout.addWidget(self.z2_input)

    def _create_wireframe_inputs(self, wireframe):
        """Cria os campos de entrada para um wireframe (polígono)."""
        self.parent.scroll_layout.addWidget(QLabel("Número de pontos:"))
        self.qtd_input = QSpinBox(self.parent)
        self.qtd_input.setMinimum(3)
        self.qtd_input.setMaximum(100)
        self.qtd_input.setValue(len(wireframe.coord))
        self.qtd_input.valueChanged.connect(self._generate_polygon_fields)
        self.parent.scroll_layout.addWidget(self.qtd_input)

        self.parent.scroll_layout.addLayout(self.parent.points_container)
        self._generate_polygon_fields()

    def _generate_polygon_fields(self):
        """Gera dinamicamente os campos de entrada para os pontos do polígono."""
        self._clear_layout(self.parent.points_container)
        self.point_inputs = []
        qtd_pontos = self.qtd_input.value()

        for i in range(qtd_pontos):
            label = QLabel(f"Ponto {i + 1} (X, Y, Z):")
            x_input = self._create_coordinate_spinbox(self.parent.object_to_edit.coord[i][0] if i < len(self.parent.object_to_edit.coord) else 0)
            y_input = self._create_coordinate_spinbox(self.parent.object_to_edit.coord[i][1] if i < len(self.parent.object_to_edit.coord) else 0)
            z_input = self._create_coordinate_spinbox(self.parent.object_to_edit.coord[i][2] if i < len(self.parent.object_to_edit.coord) else 0)
            self.point_inputs.append((x_input, y_input, z_input))
            self.parent.points_container.addWidget(label)
            self.parent.points_container.addWidget(x_input)
            self.parent.points_container.addWidget(y_input)
            self.parent.points_container.addWidget(z_input)
        self.parent.scroll_widget.setLayout(self.parent.scroll_layout)

    def _create_bezier_inputs(self, bezier):
        """Cria os campos de entrada para a curva de Bézier."""
        self.parent.scroll_layout.addWidget(QLabel("Número de pontos de controle:"))
        self.num_control_points_input = QSpinBox(self.parent)
        self.num_control_points_input.setMinimum(2)  # Bézier precisa de pelo menos 2 pontos
        self.num_control_points_input.setMaximum(100)  # Define um limite máximo razoável
        self.num_control_points_input.setValue(len(bezier.coord))
        self.num_control_points_input.valueChanged.connect(self._generate_bezier_fields)
        self.parent.scroll_layout.addWidget(self.num_control_points_input)

        self.parent.scroll_layout.addLayout(self.parent.control_points_container)
        self._generate_bezier_fields()

    def _generate_bezier_fields(self):
        """Gera dinamicamente os campos de entrada para os pontos de controle da Bézier em 3D."""
        self._clear_layout(self.parent.control_points_container)
        self.control_point_inputs = []
        num_control_points = self.num_control_points_input.value()

        for i in range(num_control_points):
            label = QLabel(f"Ponto de Controle {i + 1} (X, Y, Z):")
            x_val = self.parent.object_to_edit.coord[i][0] if i < len(self.parent.object_to_edit.coord) else 0
            y_val = self.parent.object_to_edit.coord[i][1] if i < len(self.parent.object_to_edit.coord) else 0
            z_val = self.parent.object_to_edit.coord[i][2] if i < len(self.parent.object_to_edit.coord) else 0

            x_input = self._create_coordinate_spinbox(x_val)
            y_input = self._create_coordinate_spinbox(y_val)
            z_input = self._create_coordinate_spinbox(z_val)

            self.control_point_inputs.append((x_input, y_input, z_input))
            self.parent.control_points_container.addWidget(label)
            self.parent.control_points_container.addWidget(x_input)
            self.parent.control_points_container.addWidget(y_input)
            self.parent.control_points_container.addWidget(z_input)

        self.parent.scroll_widget.setLayout(self.parent.scroll_layout)

    def _create_bspline_inputs(self, bspline):
        """Cria os campos de entrada para a curva B-Spline."""
        self.parent.scroll_layout.addWidget(QLabel("Número de pontos de controle:"))
        self.num_bspline_points_input = QSpinBox(self.parent)
        self.num_bspline_points_input.setMinimum(4)
        self.num_bspline_points_input.setMaximum(100)
        self.num_bspline_points_input.setValue(len(bspline.coord))
        self.num_bspline_points_input.valueChanged.connect(self._generate_bspline_fields)
        self.parent.scroll_layout.addWidget(self.num_bspline_points_input)

        self.parent.scroll_layout.addLayout(self.parent.bspline_points_container)
        self._generate_bspline_fields()

    def _generate_bspline_fields(self):
        """Gera dinamicamente os campos de entrada para os pontos de controle da B-Spline em 3D."""
        self._clear_layout(self.parent.bspline_points_container)
        self.bspline_point_inputs = []
        num_control_points = self.num_bspline_points_input.value()

        for i in range(num_control_points):
            label = QLabel(f"Ponto de Controle {i + 1} (X, Y, Z):")
            x_val = self.parent.object_to_edit.coord[i][0] if i < len(self.parent.object_to_edit.coord) else 0
            y_val = self.parent.object_to_edit.coord[i][1] if i < len(self.parent.object_to_edit.coord) else 0
            z_val = self.parent.object_to_edit.coord[i][2] if i < len(self.parent.object_to_edit.coord) else 0

            x_input = self._create_coordinate_spinbox(x_val)
            y_input = self._create_coordinate_spinbox(y_val)
            z_input = self._create_coordinate_spinbox(z_val)

            self.bspline_point_inputs.append((x_input, y_input, z_input))
            self.parent.bspline_points_container.addWidget(label)
            self.parent.bspline_points_container.addWidget(x_input)
            self.parent.bspline_points_container.addWidget(y_input)
            self.parent.bspline_points_container.addWidget(z_input)

        self.parent.scroll_widget.setLayout(self.parent.scroll_layout)

    def _create_object3d_inputs(self, obj):
        """Cria os campos de entrada para um objeto 3D generico (X, Y, Z)."""
        self.parent.scroll_layout.addWidget(QLabel("Número de arestas:"))
        self.qtd_input = QSpinBox(self.parent)
        self.qtd_input.setMinimum(1)
        self.qtd_input.setMaximum(100)
        self.qtd_input.setValue(len(obj.coord)/2)
        self.qtd_input.valueChanged.connect(self._generate_object3d_fields)
        self.parent.scroll_layout.addWidget(self.qtd_input)

        self.parent.points_container = QtWidgets.QVBoxLayout()
        self.parent.scroll_layout.addLayout(self.parent.points_container)
        self._generate_object3d_fields()

    def _generate_object3d_fields(self):
        """Gera dinamicamente os campos de entrada para os pontos do objeto 3D."""
        self._clear_layout(self.parent.points_container)
        self.point3d_inputs = []
        qtd_pontos = self.qtd_input.value()*2

        for i in range(qtd_pontos):
            label = QLabel(f"Ponto {i + 1} (X, Y, Z):")
            x_val = self.parent.object_to_edit.coord[i][0] if i < len(self.parent.object_to_edit.coord) else 0
            y_val = self.parent.object_to_edit.coord[i][1] if i < len(self.parent.object_to_edit.coord) else 0
            z_val = self.parent.object_to_edit.coord[i][2] if i < len(self.parent.object_to_edit.coord) else 0

            x_input = self._create_coordinate_spinbox(x_val)
            y_input = self._create_coordinate_spinbox(y_val)
            z_input = self._create_coordinate_spinbox(z_val)

            self.point3d_inputs.append((x_input, y_input, z_input))
            self.parent.points_container.addWidget(label)
            self.parent.points_container.addWidget(x_input)
            self.parent.points_container.addWidget(y_input)
            self.parent.points_container.addWidget(z_input)
        self.parent.scroll_widget.setLayout(self.parent.scroll_layout)

    def get_point_coordinates(self):
        if hasattr(self, 'x_input') and hasattr(self, 'y_input') and hasattr(self, 'z_input'):
            x_str = self.x_input.text().strip()
            y_str = self.y_input.text().strip()
            z_str = self.y_input.text().strip()
            if self._is_valid_number(x_str) and self._is_valid_number(y_str) and self._is_valid_number(z_str):
                return int(x_str), int(y_str), int(z_str)
            else:
                Wnr.noPoints()
                return None
        return None

    def get_line_coordinates(self):
        if all(hasattr(self, attr) for attr in ['x1_input', 'y1_input', 'z1_input', 'x2_input', 'y2_input', 'z2_input']):
            x1_str = self.x1_input.text().strip()
            y1_str = self.y1_input.text().strip()
            z1_str = self.z1_input.text().strip()
            x2_str = self.x2_input.text().strip()
            y2_str = self.y2_input.text().strip()
            z2_str = self.z2_input.text().strip()
            if all(self._is_valid_number(s) for s in [x1_str, y1_str, z1_str, x2_str, y2_str, z2_str]):
                return (int(x1_str), int(y1_str), int(z1_str)), (int(x2_str), int(y2_str), int(z2_str))
            else:
                Wnr.noPoints()
                return None
        return None

    def get_polygon_coordinates(self):
        if hasattr(self, 'point_inputs'):
            pontos = []
            valid = True
            for x_input, y_input, z_input in self.point_inputs:
                x_str = x_input.text().strip()
                y_str = y_input.text().strip()
                z_str = z_input.text().strip()
                if self._is_valid_number(x_str) and self._is_valid_number(y_str) and self._is_valid_number(z_str):
                    pontos.append((int(x_str), int(y_str), int(z_str)))
                else:
                    valid = False
                    break
            if valid and pontos:
                return pontos
            else:
                Wnr.noPoints()
                return None
        return None
    
    def get_bezier_coordinates(self):
        if hasattr(self, 'control_point_inputs'):
            control_points = []
            valid = True
            for x_input, y_input, z_input in self.control_point_inputs:
                x_str = x_input.text().strip()
                y_str = y_input.text().strip()
                z_str = z_input.text().strip()
                if self._is_valid_number(x_str) and self._is_valid_number(y_str) and self._is_valid_number(z_str):
                    control_points.append((int(x_str), int(y_str), int(z_str)))
                else:
                    valid = False
                    break
            if valid and control_points:
                return control_points
            else:
                Wnr.noPoints()
                return None
        return None

    def get_bspline_coordinates(self):
        if hasattr(self, 'bspline_point_inputs'):
            control_points = []
            valid = True
            for x_input, y_input, z_input in self.bspline_point_inputs:
                x_str = x_input.text().strip()
                y_str = y_input.text().strip()
                z_str = z_input.text().strip()
                if self._is_valid_number(x_str) and self._is_valid_number(y_str) and self._is_valid_number(z_str):
                    control_points.append((int(x_str), int(y_str), int(z_str)))
                else:
                    valid = False
                    break
            if valid and control_points:
                return control_points
            else:
                Wnr.noPoints()
                return None
        return None
   
    def get_object3d_coordinates(self):
        if hasattr(self, 'point3d_inputs') and self.point3d_inputs:
            coordinates = []
            valid = True
            for x_input, y_input, z_input in self.point3d_inputs:
                x_str = x_input.text().strip()
                y_str = y_input.text().strip()
                z_str = z_input.text().strip()
                if self._is_valid_number(x_str) and self._is_valid_number(y_str) and self._is_valid_number(z_str):
                    coordinates.append((int(x_str), int(y_str), int(z_str)))
                else:
                    valid = False
                    break
            if valid and coordinates:
                return coordinates
            else:
                Wnr.noPoints()
                return None
        return None       

    def _create_coordinate_spinbox(self, value=0.0):
        """Cria um QDoubleSpinBox para entrada de coordenadas com configurações consistentes."""
        return CoordinateSpinboxCreator.create_spinbox(self.parent, value)

    def _clear_layout(self, layout):
        """Limpa todos os widgets de um layout."""
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

    def _is_valid_number(self, value_str):
        """Verifica se uma string representa um número inteiro válido."""
        try:
            int(value_str)
            return True
        except ValueError:
            return False
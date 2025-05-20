from PySide6 import QtWidgets, QtCore
from PySide6.QtWidgets import QLabel, QLineEdit
from utils.wnr import Wnr
from tools.addPoint import AddPoint
from tools.addLine import AddLine
from tools.addBezier import AddBezierCurve
from tools.addWireframe import AddWireframe
from tools.addBSpline import AddBSpline 
from tools.addObject3d import AddObject3D
from screens.colorPickerWidget import ColorPickerWidget


class AddObjectDialog(QtWidgets.QDialog):
    """Dialog for adding graphical objects (Point, Line, Polygon, Bézier, BSpline)."""

    def __init__(self, selected_object, display_file, object_list):
        super().__init__()
        self.setWindowTitle("Adicionar Objeto")  # Set window title
        self.resize(320, 400)  # Set initial window size

        self.selected_object = selected_object  # Store the selected object type
        self.display_file = display_file  # Store the display file instance
        self.object_list = object_list  # Store the object list widget

        self.main_layout = QtWidgets.QVBoxLayout(self)  # Main layout for the dialog

        self._create_name_input()  # Create input for the object's name
        self._create_scrollable_area()  # Create scrollable area for coordinates
        self._create_coordinate_inputs()  # Create coordinate input fields based on object type
        self._create_color_picker()  # Create color picker widget
        self._create_action_buttons()  # Create buttons for adding and canceling

    def _create_name_input(self):
        """Creates the input field for the object's name."""
        name_layout = QtWidgets.QHBoxLayout()
        self.name_label = QLabel("Nome:")
        self.name_input = QLineEdit()
        name_layout.addWidget(self.name_label)
        name_layout.addWidget(self.name_input)
        self.main_layout.addLayout(name_layout)

    def _create_scrollable_area(self):
        """Creates the scrollable area to hold the coordinate input fields."""

        self.scroll_area = QtWidgets.QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)  # Allow scroll area to resize its content
        self.scroll_widget = QtWidgets.QWidget()  # Widget to contain the input fields
        self.scroll_layout = QtWidgets.QVBoxLayout(self.scroll_widget)  # Layout for the input fields
        self.scroll_area.setWidget(self.scroll_widget)  # Set the widget to be scrolled

        self.main_layout.addWidget(QtWidgets.QLabel(f"Inserir coordenadas para {self.selected_object}:"))
        self.main_layout.addWidget(self.scroll_area)

    def _create_coordinate_inputs(self):
        """Creates the coordinate input fields based on the selected object type."""

        if self.selected_object == "Ponto":
            self._create_point_inputs()
        elif self.selected_object == "Reta":
            self._create_line_inputs()
        elif self.selected_object == "Polígono":
            self._create_polygon_inputs()
        elif self.selected_object == "Curva de Bézier":
            self._create_bezier_inputs()
        elif self.selected_object == "B-Spline":
            self._create_bspline_inputs()
        elif self.selected_object == "Objeto 3D":
            self._create_objeto3d_inputs()

    def _create_point_inputs(self):
        """Creates input fields for a point (X, Y, Z)."""
        self.scroll_layout.addWidget(QLabel("Coordenadas (X, Y, Z):"))

        self.x_input = self._create_coordinate_spinbox()
        self.y_input = self._create_coordinate_spinbox()
        self.z_input = self._create_coordinate_spinbox()

        self.x_input.setValue(0)
        self.y_input.setValue(0)
        self.z_input.setValue(0)

        self.scroll_layout.addWidget(self.x_input)
        self.scroll_layout.addWidget(self.y_input)
        self.scroll_layout.addWidget(self.z_input)

    def _create_line_inputs(self):
        self.scroll_layout.addWidget(QLabel("Ponto 1 (X1, Y1, Z1):"))
        self.x1_input = self._create_coordinate_spinbox()
        self.y1_input = self._create_coordinate_spinbox()
        self.z1_input = self._create_coordinate_spinbox()
        self.x1_input.setValue(0)
        self.y1_input.setValue(0)
        self.z1_input.setValue(0)
        self.scroll_layout.addWidget(self.x1_input)
        self.scroll_layout.addWidget(self.y1_input)
        self.scroll_layout.addWidget(self.z1_input)

        self.scroll_layout.addWidget(QLabel("Ponto 2 (X2, Y2, Z2):"))
        self.x2_input = self._create_coordinate_spinbox()
        self.y2_input = self._create_coordinate_spinbox()
        self.z2_input = self._create_coordinate_spinbox()
        self.x2_input.setValue(0)
        self.y2_input.setValue(0)
        self.z2_input.setValue(0)
        self.scroll_layout.addWidget(self.x2_input)
        self.scroll_layout.addWidget(self.y2_input)
        self.scroll_layout.addWidget(self.z2_input)

    def _create_polygon_inputs(self):
        """Creates input fields for a polygon (dynamically generated points)."""

        self.scroll_layout.addWidget(QLabel("Número de pontos (mínimo 3):"))
        self.num_points_input = QtWidgets.QSpinBox(self)
        self.num_points_input.setMinimum(3)
        self.num_points_input.setValue(3)
        self.num_points_input.valueChanged.connect(self._generate_polygon_point_inputs)
        self.scroll_layout.addWidget(self.num_points_input)

        self.points_container = QtWidgets.QVBoxLayout()
        self.scroll_layout.addLayout(self.points_container)
        self._generate_polygon_point_inputs()

    def _generate_polygon_point_inputs(self):
        self._clear_layout(self.points_container)

        self.point_inputs = []
        num_points = self.num_points_input.value()

        for i in range(num_points):
            label = QLabel(f"Ponto {i + 1} (X, Y, Z):")
            x_input = self._create_coordinate_spinbox()
            y_input = self._create_coordinate_spinbox()
            z_input = self._create_coordinate_spinbox()

            x_input.setValue(0)
            y_input.setValue(0)
            z_input.setValue(0)

            self.points_container.addWidget(label)
            self.points_container.addWidget(x_input)
            self.points_container.addWidget(y_input)
            self.points_container.addWidget(z_input)
            self.point_inputs.append((x_input, y_input, z_input))

        self.scroll_widget.setLayout(self.scroll_layout)

    def _create_bezier_inputs(self):
        """Creates input fields for a Bézier curve (dynamically generated control points)."""
        self.scroll_layout.addWidget(QLabel("Número de pontos de controle (mínimo 4):"))
        self.num_bezier_points_input = QtWidgets.QSpinBox(self)
        self.num_bezier_points_input.setMinimum(4)
        self.num_bezier_points_input.setValue(4)
        self.num_bezier_points_input.valueChanged.connect(self._generate_bezier_point_inputs)
        self.scroll_layout.addWidget(self.num_bezier_points_input)

        self.bezier_points_container = QtWidgets.QVBoxLayout()
        self.scroll_layout.addLayout(self.bezier_points_container)
        self._generate_bezier_point_inputs()

    def _generate_bezier_point_inputs(self):
        """Dynamically generates input fields for Bézier curve control points."""
        self._clear_layout(self.bezier_points_container)

        self.bezier_point_inputs = []
        num_points = self.num_bezier_points_input.value()

        for i in range(num_points):
            label = QLabel(f"Ponto {i + 1} (X, Y, Z):")
            x_input = self._create_coordinate_spinbox()
            y_input = self._create_coordinate_spinbox()
            z_input = self._create_coordinate_spinbox()

            x_input.setValue(0)
            y_input.setValue(0)
            z_input.setValue(0)

            self.bezier_points_container.addWidget(label)
            self.bezier_points_container.addWidget(x_input)
            self.bezier_points_container.addWidget(y_input)
            self.bezier_points_container.addWidget(z_input)
            self.bezier_point_inputs.append((x_input, y_input, z_input))
        self.scroll_widget.setLayout(self.scroll_layout)

    def _create_bspline_inputs(self):
        """Creates input fields for a B-Spline curve (dynamically generated control points)."""
        self.scroll_layout.addWidget(QLabel("Número de pontos de controle (mínimo 4):"))
        self.num_bspline_points_input = QtWidgets.QSpinBox(self)
        self.num_bspline_points_input.setMinimum(4)
        self.num_bspline_points_input.setValue(4)
        self.num_bspline_points_input.valueChanged.connect(self._generate_bspline_point_inputs)
        self.scroll_layout.addWidget(self.num_bspline_points_input)

        self.bspline_points_container = QtWidgets.QVBoxLayout()
        self.scroll_layout.addLayout(self.bspline_points_container)
        self._generate_bspline_point_inputs()

    def _generate_bspline_point_inputs(self):
        self._clear_layout(self.bspline_points_container)

        self.bspline_point_inputs = []
        num_points = self.num_bspline_points_input.value()

        for i in range(num_points):
            label = QLabel(f"Ponto de controle {i + 1} (X, Y, Z):")
            x_input = self._create_coordinate_spinbox()
            y_input = self._create_coordinate_spinbox()
            z_input = self._create_coordinate_spinbox()

            x_input.setValue(0)
            y_input.setValue(0)
            z_input.setValue(0)

            self.bspline_points_container.addWidget(label)
            self.bspline_points_container.addWidget(x_input)
            self.bspline_points_container.addWidget(y_input)
            self.bspline_points_container.addWidget(z_input)
            self.bspline_point_inputs.append((x_input, y_input, z_input))

        self.scroll_widget.setLayout(self.scroll_layout)

    def _create_objeto3d_inputs(self):
        label_layout = QtWidgets.QHBoxLayout()
        label_layout.setSpacing(2) 

        label = QLabel("Número de arestas do objeto 3D (mínimo 1):")

        tooltip_icon = QLabel("🛈")
        tooltip_icon.setToolTip(
            "Cada aresta é formada por dois pontos 3D independentes.\n"
            "Exemplo: 2 arestas → 4 pontos; 3 arestas → 6 pontos."
        )
        tooltip_icon.setStyleSheet("""
            QLabel {
                color: gray;
                font-weight: bold;
                font-size: 14px;
                margin-left: 2px;  /* margem pequena para ficar perto do label */
            }
        """)
        tooltip_icon.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        tooltip_icon.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        tooltip_icon.setAttribute(QtCore.Qt.WidgetAttribute.WA_TransparentForMouseEvents, False)

        label_layout.addWidget(label)
        label_layout.addWidget(tooltip_icon)
        label_layout.addStretch()

        self.scroll_layout.addLayout(label_layout)

        self.num_arestas_input = QtWidgets.QSpinBox(self)
        self.num_arestas_input.setMinimum(1)
        self.num_arestas_input.setValue(1)
        self.num_arestas_input.valueChanged.connect(self._generate_objeto3d_point_inputs)
        self.scroll_layout.addWidget(self.num_arestas_input)

        self.objeto3d_points_container = QtWidgets.QVBoxLayout()
        self.scroll_layout.addLayout(self.objeto3d_points_container)
        self._generate_objeto3d_point_inputs()

    def _generate_objeto3d_point_inputs(self):
        self._clear_layout(self.objeto3d_points_container)

        self.objeto3d_point_inputs = []
        num_arestas = self.num_arestas_input.value()
        num_pontos = num_arestas *2

        for i in range(num_pontos):
            label = QLabel(f"Ponto {i + 1} (X, Y, Z):")
            x_input = self._create_coordinate_spinbox()
            y_input = self._create_coordinate_spinbox()
            z_input = self._create_coordinate_spinbox()

            x_input.setValue(0)
            y_input.setValue(0)
            z_input.setValue(0)

            self.objeto3d_points_container.addWidget(label)
            self.objeto3d_points_container.addWidget(x_input)
            self.objeto3d_points_container.addWidget(y_input)
            self.objeto3d_points_container.addWidget(z_input)
            self.objeto3d_point_inputs.append((x_input, y_input, z_input))

        self.scroll_widget.setLayout(self.scroll_layout)

    def _create_coordinate_spinbox(self):
        """Creates a QDoubleSpinBox for coordinate input with consistent settings."""

        spinbox = QtWidgets.QDoubleSpinBox(self)
        spinbox.setMaximum(1000000000)
        spinbox.setMinimum(-1000000000)
        spinbox.setDecimals(0)
        return spinbox

    def _clear_layout(self, layout):
        """Clears all widgets from a given layout."""

        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

    def _create_color_picker(self):
        """Creates the color picker widget."""

        self.color_picker = ColorPickerWidget()
        self.main_layout.addWidget(self.color_picker)

    def _create_action_buttons(self):
        """Creates the action buttons (Add, Cancel)."""

        self.add_button = QtWidgets.QPushButton("Adicionar")
        self.add_button.clicked.connect(self._on_add_button_clicked)
        self.main_layout.addWidget(self.add_button)

        # Ensure buttons don't steal focus by default
        self.add_button.setAutoDefault(False)
        self.add_button.setDefault(False)

    def _on_add_button_clicked(self):
        """Handles the click event of the "Adicionar" button."""

        object_name = self.name_input.text().strip()
        if not object_name:
            Wnr.noName()  # Show error message for no name
            return

        if self.object_list and object_name in self.display_file.get_names():
            Wnr.repeatedName()  # Show error message for repeated name
            return

        selected_color = self.color_picker.get_selected_color()

        if self.selected_object == "Ponto":
            self._add_point(object_name, selected_color)
        elif self.selected_object == "Reta":
            self._add_line(object_name, selected_color)
        elif self.selected_object == "Polígono":
            self._add_polygon(object_name, selected_color)
        elif self.selected_object == "Curva de Bézier":
            self._add_bezier(object_name, selected_color)
        elif self.selected_object == "B-Spline":
            self._add_bspline(object_name, selected_color)
        elif self.selected_object == "Objeto 3D":
            self._add_object3d(object_name, selected_color)

        self.object_list.addItem(f"{object_name} ({self.selected_object})")
        self.accept()  # Close the dialog successfully

    def _add_point(self, name, color):
        """Adds a point object to the display file."""

        x_str = self.x_input.text().strip()
        y_str = self.y_input.text().strip()
        z_str = self.z_input.text().strip()

        if not x_str or not y_str or not z_str:
            Wnr.noPoints()
            return

        if not self._is_valid_number(x_str) or not self._is_valid_number(y_str) or not self._is_valid_number(z_str):
            Wnr.invalidValor()
            return

        x = int(x_str)
        y = int(y_str)
        z = int(z_str)

        add_point_tool = AddPoint()
        point = add_point_tool.create(name, [(x, y, z)], color)
        self.display_file.addObject(point)

    def _add_line(self, name, color):
        """Adds a line object to the display file."""

        x1_str = self.x1_input.text().strip()
        y1_str = self.y1_input.text().strip()
        z1_str = self.z1_input.text().strip()
        x2_str = self.x2_input.text().strip()
        y2_str = self.y2_input.text().strip()
        z2_str = self.z2_input.text().strip()

        if not x1_str or not y1_str or not x2_str or not y2_str or not z1_str or not z2_str:
            Wnr.noPoints()
            return

        if not (self._is_valid_number(x1_str) and self._is_valid_number(y1_str) and
                self._is_valid_number(x2_str) and self._is_valid_number(y2_str) and
                self._is_valid_number(z1_str) and self._is_valid_number(z2_str)):
            Wnr.invalidValor()
            return

        x1 = int(x1_str)
        y1 = int(y1_str)
        z1 = int(z1_str)
        x2 = int(x2_str)
        y2 = int(y2_str)
        z2 = int(z2_str)

        add_line_tool = AddLine()
        line = add_line_tool.create(name, [(x1, y1, z1), (x2, y2, z2)], color)
        self.display_file.addObject(line)

    def _add_polygon(self, name, color):
        """Adds a polygon object to the display file."""

        points_str = [(x.text().strip(), y.text().strip(), z.text().strip()) for x, y, z in self.point_inputs]

        if any(not x or not y or not z for x, y, z in points_str):
            Wnr.noPoints()
            return

        if any(not self._is_valid_number(x) or not self._is_valid_number(y) or not self._is_valid_number(z) for x, y, z in points_str):
            Wnr.invalidValor()
            return

        points = [(int(x), int(y), int(z)) for x, y, z in points_str]
        num_points = self.num_points_input.value()

        add_wireframe_tool = AddWireframe(num_points)
        wireframe = add_wireframe_tool.create(name, points, color)
        self.display_file.addObject(wireframe)

    def _add_bezier(self, name, color):
        points_str = [(x.text().strip(), y.text().strip(), z.text().strip()) for x, y, z in self.bezier_point_inputs]

        if any(not x or not y or not z for x, y, z in points_str):
            Wnr.noPoints()
            return

        if any(
            not self._is_valid_number(x) or
            not self._is_valid_number(y) or
            not self._is_valid_number(z)
            for x, y, z in points_str
        ):
            Wnr.invalidValor()
            return

        points = [(int(x), int(y), int(z)) for x, y, z in points_str]
        n_curves = len(points) - 1
        bezier_tool = AddBezierCurve(n_curves)

        bezier_curve = bezier_tool.create(name, points, color)
        self.display_file.addObject(bezier_curve)

    def _add_bspline(self, name, color):
        """Adds a B-Spline curve to the display file."""

        points_str = [(x.text().strip(), y.text().strip(), z.text().strip()) for x, y, z in self.bspline_point_inputs]

        if any(not x or not y or not z for x, y, z in points_str):
            Wnr.noPoints()
            return

        if any(
            not self._is_valid_number(x) or
            not self._is_valid_number(y) or
            not self._is_valid_number(z)
            for x, y, z in points_str
        ):
            Wnr.invalidValor()
            return

        points = [(int(x), int(y), int(z)) for x, y, z in points_str]
        n_curves = len(points) - 1
        bspline_tool = AddBSpline(n_curves)
        bspline_curve = bspline_tool.create(name, points, color)
        self.display_file.addObject(bspline_curve)

    def _add_object3d(self, name, color):
        points_str = [(x.text().strip(), y.text().strip(), z.text().strip()) for x, y, z in self.objeto3d_point_inputs]

        if any(not x or not y or not z for x, y, z in points_str):
            Wnr.noPoints()
            return

        if any(
            not self._is_valid_number(x) or
            not self._is_valid_number(y) or
            not self._is_valid_number(z)
            for x, y, z in points_str
        ):
            Wnr.invalidValor()
            return

        points = [(int(x), int(y), int(z)) for x, y, z in points_str]
        object3dTool = AddObject3D()
        object = object3dTool.create(name, points, color)
        self.display_file.addObject(object)

    def _is_valid_number(self, value):
        """Checks if a string represents a valid integer."""
        try:
            int(value)
            return True
        except ValueError:
            return False
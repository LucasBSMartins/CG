from PySide6 import QtWidgets
from PySide6.QtWidgets import QLabel, QLineEdit
from utils.wnr import Wnr
from tools.addPoint import AddPoint
from tools.addLine import AddLine
from screens.colorPickerWidget import ColorPickerWidget
from tools.addWireframe import AddWireframe


class AddObjectDialog(QtWidgets.QDialog):
    """Dialog for adding graphical objects (Point, Line, Polygon)."""

    def __init__(self, selected_object, display_file, object_list):
        super().__init__()
        self.setWindowTitle("Adicionar Objeto")  # Set window title
        self.resize(300, 400)  # Set initial window size

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

    def _create_point_inputs(self):
        """Creates input fields for a point (X, Y)."""
        self.scroll_layout.addWidget(QLabel("Coordenadas (X, Y):"))

        self.x_input = self._create_coordinate_spinbox()
        self.y_input = self._create_coordinate_spinbox()

        self.x_input.setValue(0)
        self.y_input.setValue(0)

        self.scroll_layout.addWidget(self.x_input)
        self.scroll_layout.addWidget(self.y_input)

    def _create_line_inputs(self):
        """Creates input fields for a line (X1, Y1, X2, Y2)."""

        self.scroll_layout.addWidget(QLabel("Ponto 1 (X1, Y1):"))
        self.x1_input = self._create_coordinate_spinbox()
        self.y1_input = self._create_coordinate_spinbox()
        self.x1_input.setValue(0)
        self.y1_input.setValue(0)
        self.scroll_layout.addWidget(self.x1_input)
        self.scroll_layout.addWidget(self.y1_input)

        self.scroll_layout.addWidget(QLabel("Ponto 2 (X2, Y2):"))
        self.x2_input = self._create_coordinate_spinbox()
        self.y2_input = self._create_coordinate_spinbox()
        self.x2_input.setValue(0)
        self.y2_input.setValue(0)
        self.scroll_layout.addWidget(self.x2_input)
        self.scroll_layout.addWidget(self.y2_input)

    def _create_polygon_inputs(self):
        """Creates input fields for a polygon (dynamically generated points)."""

        self.scroll_layout.addWidget(QLabel("Número de pontos:"))
        self.num_points_input = QtWidgets.QSpinBox(self)
        self.num_points_input.setMinimum(3)
        self.num_points_input.setValue(3)
        self.num_points_input.valueChanged.connect(self._generate_polygon_point_inputs)
        self.scroll_layout.addWidget(self.num_points_input)

        self.points_container = QtWidgets.QVBoxLayout()
        self.scroll_layout.addLayout(self.points_container)
        self._generate_polygon_point_inputs()

    def _generate_polygon_point_inputs(self):
        """Dynamically generates input fields for polygon points."""

        self._clear_layout(self.points_container)  # Clear previous point input fields

        self.point_inputs = []  # Store the coordinate inputs for each point
        num_points = self.num_points_input.value()

        for i in range(num_points):
            label = QLabel(f"Ponto {i + 1} (X, Y):")
            x_input = self._create_coordinate_spinbox()
            y_input = self._create_coordinate_spinbox()

            x_input.setValue(0)
            y_input.setValue(0)

            self.points_container.addWidget(label)
            self.points_container.addWidget(x_input)
            self.points_container.addWidget(y_input)
            self.point_inputs.append((x_input, y_input))

        self.scroll_widget.setLayout(self.scroll_layout)  # Update the scroll widget layout

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

        self.object_list.addItem(f"{object_name} ({self.selected_object})")  # Add to list widget
        self.accept()  # Close the dialog successfully

    def _add_point(self, name, color):
        """Adds a point object to the display file."""

        x_str = self.x_input.text().strip()
        y_str = self.y_input.text().strip()

        if not x_str or not y_str:
            Wnr.noPoints()
            return

        if not self._is_valid_number(x_str) or not self._is_valid_number(y_str):
            Wnr.invalidValor()
            return

        x = int(x_str)
        y = int(y_str)

        add_point_tool = AddPoint()
        point = add_point_tool.create(name, [(x, y)], color)
        self.display_file.addObject(point)

    def _add_line(self, name, color):
        """Adds a line object to the display file."""

        x1_str = self.x1_input.text().strip()
        y1_str = self.y1_input.text().strip()
        x2_str = self.x2_input.text().strip()
        y2_str = self.y2_input.text().strip()

        if not x1_str or not y1_str or not x2_str or not y2_str:
            Wnr.noPoints()
            return

        if not (self._is_valid_number(x1_str) and self._is_valid_number(y1_str) and
                self._is_valid_number(x2_str) and self._is_valid_number(y2_str)):
            Wnr.invalidValor()
            return

        x1 = int(x1_str)
        y1 = int(y1_str)
        x2 = int(x2_str)
        y2 = int(y2_str)

        add_line_tool = AddLine()
        line = add_line_tool.create(name, [(x1, y1), (x2, y2)], color)
        self.display_file.addObject(line)

    def _add_polygon(self, name, color):
        """Adds a polygon object to the display file."""

        points_str = [(x.text().strip(), y.text().strip()) for x, y in self.point_inputs]

        if any(not x or not y for x, y in points_str):
            Wnr.noPoints()
            return

        if any(not self._is_valid_number(x) or not self._is_valid_number(y) for x, y in points_str):
            Wnr.invalidValor()
            return

        points = [(int(x), int(y)) for x, y in points_str]
        num_points = self.num_points_input.value()

        add_wireframe_tool = AddWireframe(num_points)
        wireframe = add_wireframe_tool.create(name, points, color)
        self.display_file.addObject(wireframe)

    def _is_valid_number(self, value):
        """Checks if a string represents a valid integer."""
        try:
            int(value)
            return True
        except ValueError:
            return False
# edit_object_dialog.py
from PySide6 import QtWidgets
from PySide6.QtWidgets import QLabel, QLineEdit
from objects.point import Point
from objects.line import Line
from objects.wireframe import Wireframe
from objects.bezier_curve import BerzierCurve
from objects.b_spline import BSpline
from objects.object3D import Object3D
from utils.wnr import Wnr
from screens.colorPickerWidget import ColorPickerWidget
from utils.edit_object_inputs import EditObjectInputs, CoordinateSpinboxCreator

class EditObject(QtWidgets.QDialog):
    """Janela para editar as coordenadas do objeto escolhido."""

    def __init__(self, selected_object, displayFile, objectList):
        super().__init__()
        self.setWindowTitle(f"Editar {selected_object.name}")
        self.resize(320, 400)
        self.__displayFile = displayFile
        self.__objectList = objectList
        self.selected_object = selected_object
        self.object_to_edit = self.selected_object
        self.inputs_handler = EditObjectInputs(self)

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
        self._scroll_layout = QtWidgets.QVBoxLayout(self.scroll_widget)
        self.scroll_area.setWidget(self.scroll_widget)
        self.main_layout.addWidget(QtWidgets.QLabel(f"Editar coordenadas para {self.selected_object.name}:"))
        self.main_layout.addWidget(self.scroll_area)

    def _create_coordinate_inputs(self):
        """Cria os campos de entrada de coordenadas com base no tipo do objeto."""
        if isinstance(self.selected_object, Point):
            self.inputs_handler._create_point_inputs(self.object_to_edit)
        elif isinstance(self.selected_object, Line):
            self.inputs_handler._create_line_inputs(self.object_to_edit)
        elif isinstance(self.selected_object, Wireframe):
            self.inputs_handler._create_wireframe_inputs(self.object_to_edit)
        elif isinstance(self.selected_object, BerzierCurve):
            self.inputs_handler._create_bezier_inputs(self.object_to_edit)
        elif isinstance(self.selected_object, BSpline):
            self.inputs_handler._create_bspline_inputs(self.object_to_edit)
        elif isinstance(self.selected_object, Object3D):
            self.inputs_handler._create_object3d_inputs(self.object_to_edit)
        self.scroll_widget.setLayout(self._scroll_layout)

    def _create_color_picker(self):
        """Cria o widget de seleção de cor."""
        self.color_picker = ColorPickerWidget(initial_color=self.selected_object.color)
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
            coords = self.inputs_handler.get_point_coordinates()
            if coords:
                self.object_to_edit.coord = [coords]
                self.object_type = " (Ponto)"
        elif isinstance(self.selected_object, Line):
            coords = self.inputs_handler.get_line_coordinates()
            if coords:
                self.object_to_edit.coord = coords
                self.object_type = " (Reta)"
        elif isinstance(self.selected_object, Wireframe):
            coords = self.inputs_handler.get_polygon_coordinates()
            if coords:
                self.object_to_edit.coord = coords
                self.object_type = " (Polígono)"
        elif isinstance(self.selected_object, BerzierCurve):
            coords = self.inputs_handler.get_bezier_coordinates()
            if coords:
                self.object_to_edit.coord = coords
                self.object_type = " (Curva de Bézier)"
        elif isinstance(self.selected_object, BSpline):
            coords = self.inputs_handler.get_bspline_coordinates()
            if coords:
                self.object_to_edit.coord = coords
                self.object_type = " (B-Spline)"
        elif isinstance(self.selected_object, Object3D):
            coords = self.inputs_handler.get_object3d_coordinates()
            if coords:
                self.object_to_edit.coord = coords
                self.object_type = " (Objeto 3D)"

        if hasattr(self, 'object_type'):
            self.object_to_edit.name = str(nome)
            self.object_to_edit.color = selected_color
            self.accept()
        else:
            Wnr.noPoints() # Or some other appropriate error message

    def _create_coordinate_spinbox(self, value=0.0):
        """Cria um QDoubleSpinBox para entrada de coordenadas com configurações consistentes."""
        return CoordinateSpinboxCreator.create_spinbox(self, value)

    def _clear_layout(self, layout):
        """Limpa todos os widgets de um layout."""
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

    @property
    def scroll_layout(self):
        return self._get_scroll_layout()

    def _get_scroll_layout(self):
        return self._scroll_layout

    @property
    def points_container(self):
        return self._get_points_container()

    def _get_points_container(self):
        if not hasattr(self, '_points_container'):
            self._points_container = QtWidgets.QVBoxLayout()
        return self._points_container

    @property
    def control_points_container(self):
        return self._get_control_points_container()
    
    @points_container.setter
    def points_container(self, value):
        self._points_container = value

    def _get_control_points_container(self):
        if not hasattr(self, '_control_points_container'):
            self._control_points_container = QtWidgets.QVBoxLayout()
        return self._control_points_container

    @property
    def bspline_points_container(self):
        return self._get_bspline_points_container()

    def _get_bspline_points_container(self):
        if not hasattr(self, '_bspline_points_container'):
            self._bspline_points_container = QtWidgets.QVBoxLayout()
        return self._bspline_points_container
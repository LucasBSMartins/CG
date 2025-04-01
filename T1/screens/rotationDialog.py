from PySide6.QtWidgets import QLabel, QDoubleSpinBox, QGridLayout, QDialog, QPushButton, QComboBox
from tools.objectTransformator import ObjectTransformator
from utils.setting import Settings, RotationType

class RotationDialog(QDialog):
    def __init__(self, displayFile, objectList):
        super().__init__()
        self.__displayFile = displayFile
        self.__objectList = objectList
        self.setWindowTitle("Rotação")
        self.resize(200, 150)

        self.layout = QGridLayout(self)

        # Escolha do ponto de rotação
        rotation_label = QLabel("Ponto de rotação:")
        self.__rotation_type = QComboBox()
        self.__rotation_type.addItems([
            RotationType.OBJECT_CENTER.value,
            RotationType.WORLD_CENTER.value,
            RotationType.ARBITRARY_POINT.value
        ])
        self.__rotation_type.currentIndexChanged.connect(self.__rotationTypeChanged)
        
        # Input do ângulo de rotação
        angle_label = QLabel("Ângulo de rotação (graus):")
        self.__angle_input = QDoubleSpinBox()
        self.__angle_input.setRange(-360, 360)
        self.__angle_input.setSingleStep(0.1)
        self.__angle_input.setValue(0)
        
        # Labels e campos de entrada para ponto arbitrário
        self.__rotation_dx_label = QLabel("Coordenada do ponto X:")
        self.__rotation_dx_input = QDoubleSpinBox()
        self.__rotation_dx_input.setRange(Settings.min_coord(), Settings.max_coord())
        self.__rotation_dx_input.setDecimals(0)

        self.__rotation_dy_label = QLabel("Coordenada do ponto Y:")
        self.__rotation_dy_input = QDoubleSpinBox()
        self.__rotation_dy_input.setRange(Settings.min_coord(), Settings.max_coord())
        self.__rotation_dy_input.setDecimals(0)
        
        # Layout
        self.layout.addWidget(rotation_label, 0, 0)
        self.layout.addWidget(self.__rotation_type, 0, 1)
        self.layout.addWidget(angle_label, 1, 0)
        self.layout.addWidget(self.__angle_input, 1, 1)
        self.layout.addWidget(self.__rotation_dx_label, 2, 0)
        self.layout.addWidget(self.__rotation_dx_input, 2, 1)
        self.layout.addWidget(self.__rotation_dy_label, 3, 0)
        self.layout.addWidget(self.__rotation_dy_input, 3, 1)
        
        # Botão de avançar
        self.next_button = QPushButton("Avançar")
        self.next_button.clicked.connect(self.next_step)
        self.next_button.setAutoDefault(False)
        self.next_button.setDefault(False)
        self.layout.addWidget(self.next_button, 4, 1)
        
        self.__rotationTypeChanged()

    def __rotationTypeChanged(self):
        """Ativa ou desativa os campos de ponto arbitrário dependendo do tipo de rotação."""
        is_arbitrary = self.__rotation_type.currentText() == RotationType.ARBITRARY_POINT.value
        self.__rotation_dx_label.setVisible(is_arbitrary)
        self.__rotation_dx_input.setVisible(is_arbitrary)
        self.__rotation_dy_label.setVisible(is_arbitrary)
        self.__rotation_dy_input.setVisible(is_arbitrary)

    def next_step(self):
        angle = self.__angle_input.value()
        rotation_type = self.__rotation_type.currentText()

        self.__selected = self.__objectList.currentRow()
        selected_item = self.__objectList.item(self.__selected)
        selected_item_text = selected_item.text()
        object_name = selected_item_text.split(' (')[0]
        selected_object = self.__displayFile.get_object(object_name)
        transformator = ObjectTransformator(selected_object)
        
        if rotation_type == RotationType.OBJECT_CENTER.value:
            transformator.rotateObjectCenter(angle)
        elif rotation_type == RotationType.WORLD_CENTER.value:
            transformator.rotateWorldCenter(angle)
        elif rotation_type == RotationType.ARBITRARY_POINT.value:
            x = self.__rotation_dx_input.value()
            y = self.__rotation_dy_input.value()
            transformator.rotateArbitraryPoint(angle, (x, y))

        self.accept()
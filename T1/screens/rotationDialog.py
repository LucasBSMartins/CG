from PySide6.QtWidgets import QLabel, QDoubleSpinBox, QGridLayout, QDialog, QComboBox, QSpinBox, QHBoxLayout, QPushButton
from utils.setting import Settings, RotationAxis

class RotationDialog(QDialog):
    def __init__(self, displayFile, objectList):
        super().__init__()
        self.__displayFile = displayFile
        self.__objectList = objectList
        self.setWindowTitle("Rotação")
        self.resize(200, 150)

        self.layout = QGridLayout(self)
        angle_label = QLabel("Ângulo de rotação (graus):")
        self.__angle_input = QSpinBox()
        self.__angle_input.setRange(-360, 360)
        self.__angle_input.setValue(0)
    
        axis_label = QLabel("Eixo de rotação:")
        self.__rotation_axis = QComboBox()
        self.__rotation_axis.addItems([RotationAxis.X.value,
                                        RotationAxis.Y.value,
                                        RotationAxis.Z.value,
                                        RotationAxis.ARBRITRARY.value])
        self.__rotation_axis.currentIndexChanged.connect(self.__rotationAxisChanged)

        self.__arbitrary_explanation = QLabel("O eixo arbitrário é o eixo entre o centro do objeto e o ponto:")
        self.__arbitrary_explanation.setFixedHeight(20) 
        self.__rotation_x_label = QLabel("x:")
        self.__rotation_x_input = QDoubleSpinBox()
        self.__rotation_x_input.setRange(Settings.min_coord(), Settings.max_coord())
        self.__rotation_y_label = QLabel("y:")
        self.__rotation_y_input = QDoubleSpinBox()
        self.__rotation_y_input.setRange(Settings.min_coord(), Settings.max_coord())
        self.__rotation_z_label = QLabel("z:")
        self.__rotation_z_input = QDoubleSpinBox()
        self.__rotation_z_input.setRange(Settings.min_coord(), Settings.max_coord())

        self.__rotationAxisChanged()

        self.layout.addWidget(angle_label, 0, 0)
        self.layout.addWidget(self.__angle_input, 0, 1)
        self.layout.addWidget(axis_label, 1, 0)
        self.layout.addWidget(self.__rotation_axis, 1, 1)
        self.layout.addWidget(self.__arbitrary_explanation, 2, 0, 1, 2)
        coords_hbox = QHBoxLayout()
        coords_hbox.addWidget(self.__rotation_x_label)
        coords_hbox.addWidget(self.__rotation_x_input)
        coords_hbox.addWidget(self.__rotation_y_label)
        coords_hbox.addWidget(self.__rotation_y_input)
        coords_hbox.addWidget(self.__rotation_z_label)
        coords_hbox.addWidget(self.__rotation_z_input)
        self.layout.addLayout(coords_hbox, 3, 0, 1, 2)  

        self.next_button = QPushButton("Avançar")
        self.next_button.clicked.connect(self.next_step)
        self.next_button.setAutoDefault(False)
        self.next_button.setDefault(False)
        self.layout.addWidget(self.next_button, 4, 1)
    
    def __rotationAxisChanged(self):
        if self.__rotation_axis.currentText() == RotationAxis.ARBRITRARY.value:
            self.__rotation_x_input.setEnabled(True)
            self.__rotation_y_input.setEnabled(True)
            self.__rotation_z_input.setEnabled(True)
            self.__rotation_x_input.show()
            self.__rotation_y_input.show()
            self.__rotation_z_input.show()
            self.__rotation_x_label.show()
            self.__rotation_y_label.show()
            self.__rotation_z_label.show()
            self.__arbitrary_explanation.show()
        else:
            self.__rotation_x_input.setEnabled(False)
            self.__rotation_y_input.setEnabled(False)
            self.__rotation_z_input.setEnabled(False)
            self.__rotation_x_input.hide()
            self.__rotation_y_input.hide()
            self.__rotation_z_input.hide()
            self.__rotation_x_label.hide()
            self.__rotation_y_label.hide()
            self.__rotation_z_label.hide()
            self.__arbitrary_explanation.hide()

    def next_step(self):
        self.__selected = self.__objectList.currentRow()
        selected_item = self.__objectList.item(self.__selected)
        selected_item_text = selected_item.text()
        object_name = selected_item_text.split(' (')[0]
        selected_object = self.__displayFile.get_object(object_name)
                    
        rotation_axis = self.__rotation_axis.currentText()
        theta = self.__angle_input.value()

        if rotation_axis == RotationAxis.X.value:
            selected_object.rotateXAxis(theta)
        elif rotation_axis == RotationAxis.Y.value:
            selected_object.rotateYAxis(theta)
        elif rotation_axis == RotationAxis.Z.value:
            selected_object.rotateZAxis(theta)
        elif rotation_axis == RotationAxis.ARBRITRARY.value:
            point = (self.__rotation_x_input.value(), self.__rotation_y_input.value(), self.__rotation_z_input.value())
            selected_object.rotateArbitrary(theta, point)
        self.accept()
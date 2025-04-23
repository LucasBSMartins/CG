from PySide6.QtWidgets import QColorDialog, QPushButton, QHBoxLayout, QWidget
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor

class ColorPickerWidget(QWidget):
    def __init__(self, initial_color="#000000", parent=None):
        super().__init__(parent)

        self.color = initial_color# Cor inicial (preto)

        # Layout horizontal para botão de cor e botão de seleção
        self.layout = QHBoxLayout(self)
        self.layout.setAlignment(Qt.AlignLeft)
        # Botão que mostra a cor escolhida
        self.color_display = QPushButton("")
        self.color_display.setFixedSize(40, 40)
        self.color_display.setStyleSheet(f"background-color: {self.color}; border-radius: 5px;")
        self.color_display.setEnabled(False)  # Apenas exibe a cor

        # Botão que abre o seletor de cores
        self.pick_color_button = QPushButton("Cor")
        self.pick_color_button.clicked.connect(self.choose_color)
        self.pick_color_button.setFixedSize(50, 30)
        self.pick_color_button.setAutoDefault(False)
        self.pick_color_button.setDefault(False)

        # Adiciona os botões ao layout
        self.layout.addWidget(self.color_display)
        self.layout.addWidget(self.pick_color_button)

    def choose_color(self):
        color = QColorDialog.getColor()
        if color.isValid():  # Se o usuário escolher uma cor válida
            self.color = color.name()  # Obtém a cor em formato HEX
            self.color_display.setStyleSheet(f"background-color: {self.color}; border-radius: 5px;")

    def get_selected_color(self):
        return self.color  # Retorna a cor escolhida

    def set_selected_color(self, color_value):
        """Define a cor exibida no widget.

        Args:
            color_value (str or tuple or list or QColor): A cor a ser definida.
                Pode ser uma string no formato HEX ('#RRGGBB'), uma tupla/lista RGB (inteiros de 0 a 255),
                ou um objeto QColor.
        """
        if isinstance(color_value, str):
            color = QColor(color_value)
            if color.isValid():
                self._color = color.name()
                self.color_display.setStyleSheet(f"background-color: {self._color}; border-radius: 5px;")
        elif isinstance(color_value, (tuple, list)) and len(color_value) == 3 and all(0 <= c <= 255 for c in color_value):
            color = QColor(*color_value)
            self._color = color.name()
            self.color_display.setStyleSheet(f"background-color: {self._color}; border-radius: 5px;")
        elif isinstance(color_value, QColor) and color.isValid():
            self._color = color.name()
            self.color_display.setStyleSheet(f"background-color: {self._color}; border-radius: 5px;")
        else:
            print(f"Aviso: Valor de cor inválido fornecido: {color_value}")
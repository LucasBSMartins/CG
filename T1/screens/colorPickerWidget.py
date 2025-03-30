from PySide6.QtWidgets import QColorDialog, QPushButton, QHBoxLayout, QWidget
from PySide6.QtCore import Qt

class ColorPickerWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.color = "#000000"  # Cor inicial (preto)

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

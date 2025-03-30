from PySide6.QtWidgets import QMessageBox

class Wnr():
    def noName():
        """Exibe mensagem de aviso para nome vazio."""
        message = QMessageBox()
        message.setWindowTitle("Aviso")
        message.setText("Dê um nome ao objeto")
        message.setIcon(QMessageBox.Warning)
        message.setStyleSheet("background-color: rgb(212,208,200); color: black;")
        message.setFixedSize(400, 200)
        message.exec()

    def repeatedName():
        """Exibe mensagem de aviso para nome repetido."""
        message = QMessageBox()
        message.setWindowTitle("Aviso")
        message.setText("Esse nome já existe")
        message.setIcon(QMessageBox.Warning)
        message.setStyleSheet("background-color: rgb(212,208,200); color: black;")
        message.setFixedSize(400, 200)
        message.exec()

    def noPoints():
        """Exibe mensagem de aviso quando os pontos não foram preenchidos."""
        message = QMessageBox()
        message.setWindowTitle("Aviso")
        message.setIcon(QMessageBox.Warning)
        message.setText("Por favor, preencha todas as coordenadas.")
        message.setStyleSheet("background-color: rgb(212,208,200); color: black;")
        message.setFixedSize(400, 200)
        message.exec()

    def show_selection_error():
        message = QMessageBox()
        message.setWindowTitle("Aviso")
        message.setIcon(QMessageBox.Warning)
        message.setText("Selecione um objeto na lista de objetos para realizar uma operação")
        message.setStyleSheet("background-color: rgb(212,208,200); color: black;")
        message.setFixedSize(400, 200)
        message.exec()

    def invalidValor():
        message = QMessageBox()
        message.setWindowTitle("Aviso")
        message.setIcon(QMessageBox.Warning)
        message.setText("Valor inválido!")
        message.setStyleSheet("background-color: rgb(212,208,200); color: black;")
        message.setFixedSize(400, 200)
        message.exec()
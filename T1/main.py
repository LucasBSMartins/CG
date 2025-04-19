import sys
from main_interface.mainWindow import MainWindow
from PySide6.QtWidgets import QApplication

'''
def run_app():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    import hupper
    hupper.start_reloader("main.run_app")

'''
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

from PySide6.QtWidgets import QMessageBox
from editObject import EditObject
from operations import Operations
from addDialog import ObjectSelectionDialog
from PySide6 import QtWidgets, QtGui
from window import Window
from viewport import Viewport
from displayFile import DisplayFile
from setting import Settings
from moveToSecondMonitor import MoveMonitor

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.__display_file = DisplayFile()
        self.__window = Window()
        self.__console = None
        
        self.setFixedSize(800, 600)
        self.setWindowTitle("SGI")
        self.setStyleSheet(f"{Settings.backgroundColor()};")
        
        self.__painter()
        #Comentar se não tiver um segundo monitor, botei só pra me ajudar 
        #MoveMonitor.center_on_second_monitor(self)

    # Contrução de frames
    def __buildFrame(self, parent, x, y, w, h):
        frame = QtWidgets.QFrame(parent)
        frame.setGeometry(x, y, w, h)
        frame.setStyleSheet("QFrame { border: 2px solid black; }")
        return frame

    def __buildText(self, text, parent, x, y, w, h):
        label = QtWidgets.QLabel(text, parent)
        label.setGeometry(x, y, w, h)
        label.setStyleSheet(f"{Settings.backgroundColor()}; color: black; border: none;")
        return label
            
    # Construção dos botões de controle da window (movimentação e zoom)
    def __createControlFrameButton(self, path_icon, function, text):
        button = QtWidgets.QPushButton(path_icon, self.__control_frame)
        button.setToolTip(text)
        button.clicked.connect(function)
        button.setStyleSheet("""
        QPushButton {
            background-color: rgb(200, 200, 200); 
            color: black; 
            border: 1px solid black;
        }
        """)
        return button
    
    # Construção dos botões do frame de objetos
    def __createObjectFrameButton(self, name, function):
        button = QtWidgets.QPushButton(name, self.__buttons_frame)
        button.clicked.connect(function)
        button.setStyleSheet("""
        QPushButton {
            background-color: rgb(200, 200, 200); 
            color: black; 
            border: 1px solid black;
        }
        """)
         
        return button

    def  __painter(self):
        
        # ///////////////// Gerando delimitações de área //////////////////////
        self.__menu_frame = self.__buildFrame(self, Settings.menu_frame()[0],
                                         Settings.menu_frame()[1],
                                         Settings.menu_frame()[2],
                                         Settings.menu_frame()[3])
        
        self.__console_frame = self.__buildFrame(self, 250, 490, 530, 90)
        
        self.__view_frame = self.__buildFrame(self, Settings.canvas()[0],
                                         Settings.canvas()[1],
                                         Settings.canvas()[2],
                                         Settings.canvas()[3])

        self.__objects_frame = self.__buildFrame(self.__menu_frame, Settings.objects_frame()[0],
                                         Settings.objects_frame()[1],
                                         Settings.objects_frame()[2],
                                         Settings.objects_frame()[3])
        self.__objects_frame.setStyleSheet(f"{Settings.backgroundColor()}; border: false")

        self.__buttons_frame= self.__buildFrame(self.__menu_frame, Settings.buttons_frame()[0],
                                                    Settings.buttons_frame()[1],
                                                    Settings.buttons_frame()[2],
                                                    Settings.buttons_frame()[3])
        self.__buttons_frame.setStyleSheet(f"{Settings.backgroundColor()}; border: true")

        self.__control_frame= self.__buildFrame(self.__menu_frame, Settings.control_frame()[0],
                                                    Settings.control_frame()[1],
                                                    Settings.control_frame()[2],
                                                    Settings.control_frame()[3])
        
        # ///////////////// ////////////////////// //////////////////////

        # ///////////////// Coisas que usamos //////////////////////

        self.__console = QtWidgets.QTextEdit(self.__console_frame)
        self.__console.setReadOnly(True)
        self.__console.setStyleSheet("color: black; background-color: white; border: 1px solid black;")
        self.__console.setGeometry(5, 5, 520, 80)

        # Viewport
        self.__viewport = Viewport(self.__view_frame, self.__window)  

        self.__object_list = QtWidgets.QListWidget(self.__objects_frame)
        self.__object_list.setGeometry(5, 10, 190, 150)
        self.__object_list.setStyleSheet("background-color: white; color: black; border: 1px solid black;")

        # ///////////////// ////////////////////// //////////////////////

        # ///////////////// Gerando labels //////////////////////
        self.__messages_label = QtWidgets.QLabel(f"A WINDOW ESTÁ EM X: {self.__window.xw_min} a {self.__window.xw_max}   Y: {self.__window.yw_min} a {self.__window.yw_max}", self.__view_frame)
        self.__messages_label.setStyleSheet("color: black; border: true;")
        self.__messages_label.setWordWrap(True)
        self.__messages_label.setGeometry(10, 440, 500, 15)
               
        self.__viewport_label = self.__buildText("  VIEWPORT", self.__view_frame,
                                          Settings.canvas()[0] - 235, Settings.canvas()[1] - 25, 70, 20)

        self.__menu_label = self.__buildText("   MENU DE FUNÇÕES", self.__menu_frame,
                                           10, Settings.menu_frame()[1] - 25, 125, 20)
        
        self.__objects_label = self.__buildText(" OBJETOS", self.__menu_frame,
                                           15, Settings.objects_frame()[1] - 10, 60, 20)
        
        self.__objects_label = self.__buildText(" WINDOW", self.__menu_frame,
                                           25, Settings.control_frame()[1] - 10, 60, 20)

        # ///////////////// ////////////////////// //////////////////////

        # ///////////////// Gerando botões //////////////////////

        # Botões objetos
        self.__add_button = self.__createObjectFrameButton('ADICIONAR', lambda: self.__add_object())
        self.__operations_button = self.__createObjectFrameButton('OPERAÇÕES', self.__choose_operation)

        self.__add_button.setGeometry(0, 0, 90, 25) 
        self.__operations_button.setGeometry(100, 0, 90, 25)   

        # Botões controle da Window

        self.__scaleSpinBox = QtWidgets.QDoubleSpinBox(self.__control_frame)
        self.__scaleSpinBox.setGeometry(10, 30, 80, 25)
        self.__scaleSpinBox.setRange(0.01, 99.99)
        self.__scaleSpinBox.setSingleStep(1)
        self.__scaleSpinBox.setSuffix("%")
        self.__scaleSpinBox.setValue(10.0)
        self.__scaleSpinBox.setStyleSheet("background-color: white")


        self.__zoom_in_button = self.__createControlFrameButton("ZOOM +", lambda: self.__zoomIn(), "Zoom in")
        self.__zoom_in_button.setGeometry(100, 15, 80, 25)
        self.__zoom_out_button = self.__createControlFrameButton("ZOOM -", lambda: self.__zoomOut(), "Zoom out")
        self.__zoom_out_button.setGeometry(100, 45, 80, 25)

        self.__up_button = self.__createControlFrameButton("↑", lambda: self.__moveUp(), "Mover window para cima")
        self.__up_button.setGeometry(75, 100, 40, 40)
        self.__down_button = self.__createControlFrameButton("↓", lambda: self.__moveDown(), "Mover window para baixo" )
        self.__down_button.setGeometry(75, 145, 40, 40)
        self.__left_button = self.__createControlFrameButton("←", lambda: self.__moveLeft(), "Mover window para esquerda")
        self.__left_button.setGeometry(30, 145, 40, 40)
        self.__right_button = self.__createControlFrameButton("→", lambda: self.__moveRight(), "Mover window para direita")
        self.__right_button.setGeometry(120, 145, 40, 40)

        # ///////////////// ////////////////////// //////////////////////


    def __updateViewframe(self):
        self.__messages_label.setText(
                f"A WINDOW ESTÁ EM X: {self.__window.xw_min:.2f} a {self.__window.xw_max:.2f}   "
                f"Y: {self.__window.yw_min:.2f} a {self.__window.yw_max:.2f}"
            )   
        self.__viewport.drawViewportObj(self.__display_file.objects_list)

    def log_message(self, message):
        self.__console.append(message)
        self.__updateViewframe()

    def __add_object(self):
        add_dialog = ObjectSelectionDialog(self.__display_file, self.__object_list)
        add_dialog.exec()
        self.__updateViewframe()

    def __choose_operation(self):
        selected_index = self.__object_list.currentRow()

        if selected_index == -1:
            self.__show_selection_error()
        else:
            self.__perform_selected_operation(selected_index)

    def __show_selection_error(self):
        message = QMessageBox()
        message.setWindowTitle("Aviso")
        message.setIcon(QMessageBox.Warning)
        message.setText("Selecione um objeto na lista de objetos para realizar uma operação")
        message.setStyleSheet("background-color: rgb(212,208,200); color: black;")
        message.setFixedSize(400, 200)
        message.exec()

    def __perform_selected_operation(self, selected_index):
        object_name = self.__object_list.item(selected_index).text()
        operations = Operations(object_name)
        if operations.exec() == QtWidgets.QDialog.DialogCode.Accepted:
            self.__handle_operation(operations.clicked_button, selected_index)

    def __handle_operation(self, clicked_button, selected_index):
        if clicked_button == "delete":
            self.__deleteObject(selected_index)
        elif clicked_button == "edit":
            self.__editObject(selected_index)

    def __deleteObject(self, index_selected_obj):
        index_selected_obj = self.__object_list.currentRow()      
        if index_selected_obj != -1:
            selected_item = self.__object_list.item(index_selected_obj)
            selected_item_text = selected_item.text()
            object_name = selected_item_text.split(' (')[0]
            self.log_message(f"Objeto {object_name} deletado.")

        self.__object_list.takeItem(index_selected_obj)
        self.__display_file.removeObject(index_selected_obj)
        self.__updateViewframe()
    
    def __editObject(self, index_selected_obj):
        index_selected_obj = self.__object_list.currentRow()      
        if index_selected_obj != -1:
            selected_item = self.__object_list.item(index_selected_obj)
            if selected_item:
                selected_item_text = selected_item.text()
                object_name = selected_item_text.split(' (')[0]
                selected_object = self.__display_file.get_object(object_name)
                
                if selected_object:
                    edit_window = EditObject(selected_object, self.__display_file, self.__object_list)
                    
                    if edit_window.exec() == QtWidgets.QDialog.DialogCode.Accepted:
                        self.log_message(f"Objeto {object_name} editado.")
                        self.__updateViewframe()
                else:
                    self.log_message("Object not found.")
            else:
                self.log_message("No selected item.")
        else:
            self.log_message("No object selected.")

    def __moveLeft(self):
        self.__window.move("left", self.__scaleSpinBox.value())
        self.log_message(f"Window foi movida pra esquerda em {self.__scaleSpinBox.value()}%.")
        self.__updateViewframe()
    
    # Movimentação para direita
    def __moveRight(self):
        self.__window.move("right", self.__scaleSpinBox.value())
        self.log_message(f"Window foi movida pra direita em {self.__scaleSpinBox.value()}%.")
        self.__updateViewframe()

    # Movimentação para cima
    def __moveUp(self):
        self.__window.move("up", self.__scaleSpinBox.value())
        self.log_message(f"Window foi movida pra cima em {self.__scaleSpinBox.value()}%.")
        self.__updateViewframe()
    
    # Movimentação para baixo
    def __moveDown(self):
        self.__window.move("down", self.__scaleSpinBox.value())
        self.log_message(f"Window foi movida pra baixo em {self.__scaleSpinBox.value()}%.")
        self.__updateViewframe()
    
    # ZoomIn
    def __zoomIn(self):
        self.__window.zoomIn(self.__scaleSpinBox.value())
        self.log_message(f"Zoom In de {self.__scaleSpinBox.value()}% aplicado.")
        self.__updateViewframe()
    
    # ZoomOut
    def __zoomOut(self):
        self.__window.zoomOut(self.__scaleSpinBox.value())
        self.log_message(f"Zoom Out de {self.__scaleSpinBox.value()}% aplicado.")
        self.__updateViewframe()
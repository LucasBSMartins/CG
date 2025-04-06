from tools.windowControls import WindowControls
from tools.objectEditor import ObjectEditor
from screens.operations import Operations
from screens.objectSelectionDialog import ObjectSelectionDialog
from PySide6 import QtWidgets, QtGui, QtCore
from utils.wnr import Wnr
from utils.logs import Logs
from main_interface.window import Window
from main_interface.viewport import Viewport
from main_interface.displayFile import DisplayFile
from utils.setting import Settings
from utils.moveToSecondMonitor import MoveMonitor
from screens.transformObjectDialog import TransformObjectDialog

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.__display_file = DisplayFile()
        self.__window = Window()
        self.__console = None
        
        # Define tamanho fixo da janela, nome e cor
        self.setFixedSize(800, 610)
        self.setWindowTitle("SGI")
        self.setStyleSheet(f"{Settings.backgroundColor()};")
        
        self.__painter()

        MoveMonitor.center_on_second_monitor(self)

    # Contrução de frames
    def __buildFrame(self, parent, x, y, w, h):
        frame = QtWidgets.QFrame(parent)
        frame.setGeometry(x, y, w, h)
        frame.setStyleSheet("QFrame { border: 2px solid black; }")
        return frame

    # Método para criar e configurar um texto (QLabel) dentro de um frame
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

        # Criando e posicionando os frames principais
        self.__menu_frame = self.__buildFrame(self, Settings.menu_frame()[0],
                                         Settings.menu_frame()[1],
                                         Settings.menu_frame()[2],
                                         Settings.menu_frame()[3])
        
        self.__console_frame = self.__buildFrame(self, 250, 500, 530, 90)
        
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

        # Criando o console de saída
        self.__console = QtWidgets.QTextEdit(self.__console_frame)
        self.__console.setReadOnly(True)
        self.__console.setStyleSheet("color: black; background-color: white; border: 1px solid black;")
        self.__console.setGeometry(5, 5, 520, 80)

        #Criando viewport
        self.__viewport = Viewport(self.__view_frame, self.__window)  

        # Criando lista de objetos
        self.__object_list = QtWidgets.QListWidget(self.__objects_frame)
        self.__object_list.setGeometry(5, 5, 190, 150)
        self.__object_list.setStyleSheet("background-color: white; color: black; border: 1px solid black;")
    
        # Criando sistema de logs
        log_message_func = self.__log_message
        self.__logs = Logs(log_message_func, self.__object_list)
        toolbar = QtWidgets.QToolBar("Main Menu")
        toolbar.setMovable(False)
        self.addToolBar(QtCore.Qt.TopToolBarArea, toolbar)

        menu = QtWidgets.QMenu("Options", self)
        import_action = QtGui.QAction("Import", self)
        export_action = QtGui.QAction("Export", self)
        menu.addAction(import_action)
        menu.addAction(export_action)

        menu.setStyleSheet(Settings.menuStyleSheet())

        # Connect the actions in the menu to their respective functions
        #import_action.triggered.connect(self.handle_import)  # Replace self.handle_import with your function
       # export_action.triggered.connect(self.handle_export)

        menu_action = QtGui.QAction("Options", self)
        menu_action.setMenu(menu)
        menu_button = QtWidgets.QToolButton()
        menu_button.setDefaultAction(menu_action)
        menu_button.setPopupMode(QtWidgets.QToolButton.InstantPopup)
        toolbar.addWidget(menu_button)

        toolbar.setIconSize(QtCore.QSize(16, 16))
        toolbar.setStyleSheet("QToolBar { spacing: 4px; padding: 2px; }")
        toolbar.setFixedHeight(20)
        menu_button.setFixedSize(60, 20)
        menu_button.setStyleSheet(Settings.menuButtonStyleSheet())
        # ///////////////// ////////////////////// //////////////////////

        # ///////////////// Gerando labels //////////////////////
              
        self.__viewport_label = self.__buildText("  VIEWPORT", self.__view_frame,
                                          Settings.canvas()[0] - 235, Settings.canvas()[1] - 35, 70, 20)

        self.__menu_label = self.__buildText("   MENU DE FUNÇÕES", self.__menu_frame,
                                           10, Settings.menu_frame()[1] - 35, 125, 20)
        
        self.__objects_label = self.__buildText(" OBJETOS", self.__menu_frame,
                                           15, Settings.objects_frame()[1] - 15, 60, 20)
        
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

        window_controls = WindowControls(self.__window, self.__scaleSpinBox, self.__logs, self.__updateViewframe)

        self.__zoom_in_button = self.__createControlFrameButton("ZOOM +", lambda: window_controls.zoom_in(), "Zoom in")
        self.__zoom_in_button.setGeometry(100, 15, 80, 25)
        self.__zoom_out_button = self.__createControlFrameButton("ZOOM -", lambda: window_controls.zoom_out(), "Zoom out")
        self.__zoom_out_button.setGeometry(100, 45, 80, 25)

        self.__up_button = self.__createControlFrameButton("↑", lambda: window_controls.move_up(), "Mover window para cima")
        self.__up_button.setGeometry(75, 100, 40, 40)
        self.__down_button = self.__createControlFrameButton("↓", lambda: window_controls.move_down(), "Mover window para baixo" )
        self.__down_button.setGeometry(75, 145, 40, 40)
        self.__left_button = self.__createControlFrameButton("←", lambda: window_controls.move_left(), "Mover window para esquerda")
        self.__left_button.setGeometry(30, 145, 40, 40)
        self.__right_button = self.__createControlFrameButton("→", lambda: window_controls.move_right(), "Mover window para direita")
        self.__right_button.setGeometry(120, 145, 40, 40)

        # Campo para definir o ângulo de rotação
        self.__rotation_spinbox = QtWidgets.QDoubleSpinBox(self.__control_frame)
        self.__rotation_spinbox.setGeometry(60, 210, 70, 35)
        self.__rotation_spinbox.setRange(-360.0, 360.0)
        self.__rotation_spinbox.setSingleStep(5.0)
        self.__rotation_spinbox.setSuffix("°")
        self.__rotation_spinbox.setValue(15.0)
        self.__rotation_spinbox.setStyleSheet("background-color: white")

        # Botão de rotação anti-horária
        self.__rotate_ccw_button = self.__createControlFrameButton("⟲", lambda: window_controls.rotate_window(-self.__rotation_spinbox.value()), "Rotacionar anti-horário")
        self.__rotate_ccw_button.setGeometry(10, 210, 40, 35)

        # Botão de rotação horária
        self.__rotate_cw_button = self.__createControlFrameButton("⟳", lambda: window_controls.rotate_window(self.__rotation_spinbox.value()), "Rotacionar horário")
        self.__rotate_cw_button.setGeometry(140, 210, 40, 35)
        font = QtGui.QFont()
        font.setPointSize(15)

        self.__rotate_ccw_button.setFont(font)
        self.__rotate_cw_button.setFont(font)
        # ///////////////// ////////////////////// //////////////////////

    # Método para atualizar a exibição da janela
    def __updateViewframe(self):
        self.__viewport.drawViewportObj(self.__display_file.objects_list)

    # Método para exibir mensagens no console
    def __log_message(self, message):
        self.__console.append(message)
        self.__updateViewframe()

    # Método para adicionar um novo objeto
    def __add_object(self):
        add_dialog = ObjectSelectionDialog(self.__display_file, self.__object_list)
        add_dialog.exec()

        self.__logs.logAddObject()
        self.__updateViewframe()
    
    # Método para escolher uma operação sobre um objeto selecionado
    def __choose_operation(self):

        selected_index = self.__object_list.currentRow()
        if selected_index == -1:
            Wnr.show_selection_error()
        else:
            self.__perform_selected_operation(selected_index)

    # Método que executa a operação escolhida sobre um objeto
    def __perform_selected_operation(self, selected_index):

        object_name = self.__object_list.item(selected_index).text()
        operations = Operations(object_name)
        if operations.exec() == QtWidgets.QDialog.DialogCode.Accepted:
            self.__handle_operation(operations.clicked_button)

    # Método que decide qual operação realizar
    def __handle_operation(self, clicked_button):

        if clicked_button == "delete":
            self.__deleteObject()
        elif clicked_button == "edit":
            self.__editObject()
        elif clicked_button == "transform":
            self.__transformObject()

    def __transformObject(self):
        
        transform_dialog = TransformObjectDialog(self.__display_file, self.__object_list)
        transform_dialog.exec()
        self.__updateViewframe()

    # Método para deletar um objeto selecionado
    def __deleteObject(self):

        index_selected_obj = self.__object_list.currentRow()      
        
        self.__logs.logDeleteMessage()
        self.__object_list.takeItem(index_selected_obj)
        self.__display_file.removeObject(index_selected_obj)
        self.__updateViewframe()

    # Método para editar um objeto
    def __editObject(self):
        object_list = self.__object_list
        display_file = self.__display_file
        log_message_func = self.__logs
        update_view_func = self.__updateViewframe
        object_editor = ObjectEditor(object_list, display_file, log_message_func, update_view_func)
        object_editor.edit_object()

    def __create_options_menu(self):
        menu = QtWidgets.QMenu(self)
        import_action = QtGui.QAction("Import", self)
        export_action = QtGui.QAction("Export", self)
        menu.addAction(import_action)
        menu.addAction(export_action)
        return menu
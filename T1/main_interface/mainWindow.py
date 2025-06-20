from tools.objectEditor import ObjectEditor
from screens.operations import Operations
from tools.reader import ReaderOBJ
from tools.exporter import GenerateOBJ
from screens.objectSelectionDialog import ObjectSelectionDialog
from PySide6 import QtWidgets, QtGui, QtCore
from utils.wnr import Wnr
from utils.logs import Logs
from objects.line import Line
from objects.point import Point
from objects.wireframe import Wireframe 
from objects.object3D import Object3D
from main_interface.window import Window
from main_interface.viewport import Viewport
from main_interface.displayFile import DisplayFile
from utils.setting import Settings, ClippingAlgorithm, Projection
from utils.moveToSecondMonitor import MoveMonitor
from main_interface.canvas import Canvas
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

        #MoveMonitor.center_on_second_monitor(self)

    # Contrução de frames
    def __buildFrame(self, parent, x, y, w, h):
        frame = QtWidgets.QFrame(parent)
        frame.setGeometry(x, y, w, h)
        frame.setStyleSheet("QFrame { border: 2px solid black; }")
        return frame

    def __buildFrameBorderless(self, parent, x, y, w, h):
        frame = QtWidgets.QFrame(parent)
        frame.setGeometry(x, y, w, h)
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

    def __createControlFrameRadioButton(self, text, algorithm, x, y, width, height):
        radio_button = QtWidgets.QRadioButton(text, self.__clipping_frame)
        radio_button.setGeometry(x, y, width, height)
        radio_button.algorithm = algorithm
        radio_button.setStyleSheet("color: black;")
        return radio_button
    
    def __createControlFrameMoveRotateRadioButton(self, text, x, y, width, height):
        radio_button = QtWidgets.QRadioButton(text, self.__control_frame)
        radio_button.setGeometry(x, y, width, height)
        radio_button.setStyleSheet("color: black;")
        return radio_button

    def  __painter(self):
        
        # ///////////////// Gerando delimitações de área //////////////////////

        # Criando e posicionando os frames principais
        self.__menu_frame = self.__buildFrame(self, Settings.menu_frame()[0],
                                         Settings.menu_frame()[1],
                                         Settings.menu_frame()[2],
                                         Settings.menu_frame()[3])
        
        self.__console_frame = self.__buildFrame(self, 250, 520, 530, 70)

        self.__projection_frame = self.__buildFrameBorderless(self, 250, 492, 530, 26)
        
        self.__view_frame = self.__buildFrame(self, Settings.view_frame()[0],
                                         Settings.view_frame()[1],
                                         Settings.view_frame()[2],
                                         Settings.view_frame()[3])

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
        
        self.__clipping_frame= self.__buildFrame(self.__menu_frame, Settings.clipping_frame()[0],
                                                    Settings.clipping_frame()[1],
                                                    Settings.clipping_frame()[2],
                                                    Settings.clipping_frame()[3])

        # ///////////////// ////////////////////// //////////////////////

        # ///////////////// Coisas que usamos //////////////////////

        # Criando o console de saída
        self.__console = QtWidgets.QTextEdit(self.__console_frame)
        self.__console.setReadOnly(True)
        self.__console.setStyleSheet("color: black; background-color: white; border: 1px solid black;")
        self.__console.setGeometry(5, 5, 520, 60)

        #Criando viewport
        self.__viewport = Viewport(self.__window)

        self.__canvas = Canvas(self.__view_frame, self.__viewport)  

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

        import_action.triggered.connect(self.__importFile)
        export_action.triggered.connect(self.__exportFile)

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
                                           10, Settings.view_frame()[1] - 36, 70, 20)

        self.__menu_label = self.__buildText("   MENU DE FUNÇÕES", self.__menu_frame,
                                           10, Settings.menu_frame()[1] - 35, 125, 20)
        
        self.__objects_label = self.__buildText(" OBJETOS", self.__menu_frame,
                                           15, Settings.objects_frame()[1] - 15, 60, 20)
        
        self.__objects_label = self.__buildText(" CONTROLES", self.__menu_frame,
                                           25, Settings.control_frame()[1] - 10, 75, 20)
        
        self.__clipping_label = self.__buildText(" CLIPAGEM", self.__menu_frame,
                                           25, Settings.clipping_frame()[1] - 10, 60, 18)

        # ///////////////// ////////////////////// //////////////////////

        # ///////////////// Gerando botões //////////////////////

        # Clipping Algorithm Radio Buttons
        self.__clipping_group = QtWidgets.QButtonGroup(self.__clipping_frame)

        self.__cohen_sutherland_radio = self.__createControlFrameRadioButton(
            "Cohen-Sutherland", ClippingAlgorithm.COHEN, 5, 5, 180, 20
        )
        self.__liang_barsky_radio = self.__createControlFrameRadioButton(
            "Liang-Barsky", ClippingAlgorithm.LIANG, 5, 25, 180, 20
        )

        self.__clipping_group.addButton(self.__cohen_sutherland_radio)
        self.__clipping_group.addButton(self.__liang_barsky_radio)

        self.__cohen_sutherland_radio.setChecked(True)  # Default selection
        self.__clipping_algorithm = ClippingAlgorithm.COHEN  # Initialize the algorithm

        self.__clipping_group.buttonClicked.connect(self.__update_clipping_algorithm)
        
        # Prompt(s) empregado(s):
        #   - "Crie um grupo de botões (QButtonGroup) para gerenciar dois QRadioButtons:
        #     um para projeção paralela ('PARALLEL') e outro para projeção em perspectiva
        #     ('PERSPECTIVE'). Configure a geometria, o estado inicial (paralela marcada),
        #     e o estilo de cor para preto para ambos. Conecte o sinal 'toggled' de cada
        #     botão ao método `__changeProjection` da classe."
        #
        # Dicionário de Dados da Interface (Variáveis de Instância configuradas):
        #   - self.__parallel_button (QtWidgets.QRadioButton): Botão de rádio para projeção paralela.
        #   - self.__perspective_button (QtWidgets.QRadioButton): Botão de rádio para projeção em perspectiva.
        #   - self.__projection (Projection enum): Armazena o tipo de projeção selecionado.
        
        # Botões de projeção paralela x projeção em perspectiva
        projection_buttons = QtWidgets.QButtonGroup()
        self.__parallel_button = QtWidgets.QRadioButton(Projection.PARALLEL.value, self.__projection_frame)
        self.__parallel_button.setGeometry(0, 2, 120, 20)
        self.__parallel_button.setChecked(True)
        self.__projection = Projection.PARALLEL
        self.__parallel_button.setStyleSheet("color: black;")
        self.__parallel_button.toggled.connect(self.__changeProjection)
        self.__perspective_button = QtWidgets.QRadioButton(Projection.PERSPECTIVE.value, self.__projection_frame)
        self.__perspective_button.setGeometry(125, 2, 160, 20)
        projection_buttons.addButton(self.__parallel_button)
        projection_buttons.addButton(self.__perspective_button)
        self.__perspective_button.toggled.connect(self.__changeProjection)
        self.__perspective_button.setStyleSheet("color: black;")

        # Botões objetos
        self.__add_button = self.__createObjectFrameButton('ADICIONAR', lambda: self.__add_object())
        self.__operations_button = self.__createObjectFrameButton('OPERAÇÕES', self.__choose_operation)

        self.__add_button.setGeometry(0, 0, 90, 25) 
        self.__operations_button.setGeometry(100, 0, 90, 25)   

        self.__move_rotate_group = QtWidgets.QButtonGroup(self.__control_frame)
        self.__move_radio = self.__createControlFrameMoveRotateRadioButton("Movimentação", 5, 7, 120, 20)
        self.__rotate_radio = self.__createControlFrameMoveRotateRadioButton("Rotação", 5, 25, 180, 20)

        self.__move_rotate_group.addButton(self.__move_radio)
        self.__move_rotate_group.addButton(self.__rotate_radio)

        self.__move_radio.setChecked(True) # Default selection for move/rotate

        self.__move_rotate_group.buttonClicked.connect(self.__changeMoveRotate)

        self.__scaleSpinBox = QtWidgets.QDoubleSpinBox(self.__control_frame)
        self.__scaleSpinBox.setGeometry(10, 60, 80, 25)
        self.__scaleSpinBox.setRange(0.01, 99.99)
        self.__scaleSpinBox.setSingleStep(1)
        self.__scaleSpinBox.setSuffix("%")
        self.__scaleSpinBox.setValue(10.0)
        self.__scaleSpinBox.setStyleSheet("background-color: white")

        self.__zoom_in_button = self.__createControlFrameButton("+", lambda: self.__zoom("in"), "Zoom in")
        self.__zoom_in_button.setGeometry(100, 50, 40, 40)
        self.__zoom_in_button.setStyleSheet("font-size: 15px;")
        self.__zoom_out_button = self.__createControlFrameButton("-", lambda: self.__zoom("out"), "Zoom out")
        self.__zoom_out_button.setGeometry(142, 50, 40, 40)
        self.__zoom_out_button.setStyleSheet("font-size: 15px;")

        self.__up_button = self.__createControlFrameButton("↑", lambda: self.__moveUp(), "Mover window para cima")
        self.__up_button.setGeometry(75, 100, 40, 40)
        self.__down_button = self.__createControlFrameButton("↓", lambda: self.__moveDown(), "Mover window para baixo" )
        self.__down_button.setGeometry(75, 145, 40, 40)
        self.__left_button = self.__createControlFrameButton("←", lambda: self.__moveLeft(), "Mover window para esquerda")
        self.__left_button.setGeometry(30, 145, 40, 40)
        self.__right_button = self.__createControlFrameButton("→", lambda: self.__moveRight(), "Mover window para direita")
        self.__right_button.setGeometry(120, 145, 40, 40)
        self.__back_button = self.__createControlFrameButton("▲", lambda: self.__moveBack(), "Mover window para trás")
        self.__back_button.setGeometry(35, 105, 35, 35)
        self.__front_button = self.__createControlFrameButton("▼", lambda: self.__moveFront(), "Mover window para frente")
        self.__front_button.setGeometry(120, 105, 35, 35)

        # Campo para definir o ângulo de rotação
        self.__rotation_spinbox = QtWidgets.QDoubleSpinBox(self.__control_frame)
        self.__rotation_spinbox.setGeometry(60, 200, 70, 35)
        self.__rotation_spinbox.setRange(-360.0, 360.0)
        self.__rotation_spinbox.setSingleStep(5.0)
        self.__rotation_spinbox.setSuffix("°")
        self.__rotation_spinbox.setValue(15.0)
        self.__rotation_spinbox.setStyleSheet("background-color: white")

        # Botão de rotação anti-horária
        self.__rotate_ccw_button = self.__createControlFrameButton("⟲", lambda: self.__rotateLeft(self.__rotation_spinbox.value()), "Rotacionar anti-horário")
        self.__rotate_ccw_button.setGeometry(10, 200, 40, 35)

        # Botão de rotação horária
        self.__rotate_cw_button = self.__createControlFrameButton("⟳", lambda: self.__rotateRight(self.__rotation_spinbox.value()), "Rotacionar horário")
        self.__rotate_cw_button.setGeometry(140, 200, 40, 35)
        font = QtGui.QFont()
        font.setPointSize(15)

        self.__rotate_ccw_button.setFont(font)
        self.__rotate_cw_button.setFont(font)

        #Criando exemplos
        obj1 = Line("linha1", [(200, 0, 800), (400, 0, 800)], QtGui.QColor(0,0,0))
        self.__display_file.addObject(obj1)
        self.__object_list.addItem(str(obj1.name))
        obj2 = Wireframe("wireframe1", [(300, -200, 800), (-300, -200, 800), (0, 200, 800)], QtGui.QColor(255,0,0))
        self.__display_file.addObject(obj2)
        self.__object_list.addItem(str(obj2.name))
        obj3 = Object3D("cubo", [(-800, -800, 400), (-800, -400, 400), (-800, -400, 400), (-400, -400, 400), (-400, -400, 400), (-400, -800, 400), (-400, -800, 400), (-800, -800, 400), (-800, -800, 800), (-800, -400, 800), (-800, -400, 800), (-400, -400, 800), (-400, -400, 800), (-400, -800, 800), (-400, -800, 800), (-800, -800, 800), (-800, -800, 400), (-800, -800, 800), (-800, -400, 400), (-800, -400, 800), (-400, -800, 400), (-400, -800, 800), (-400, -400, 400), (-400, -400, 800)], QtGui.QColor(0,255,0))
        self.__display_file.addObject(obj3)
        self.__object_list.addItem(str(obj3.name))

        self.__updateViewframe()

        # ///////////////// ////////////////////// //////////////////////

    # Método para atualizar a exibição da janela
    def __updateViewframe(self):
        self.__canvas.drawObjects(self.__display_file.objects_list, self.__clipping_algorithm, self.__window, self.__projection)
  
    def __moveLeft(self):
        selected_radio = self.__move_rotate_group.checkedButton()
        if selected_radio == self.__move_radio:
            self.__window.moveLeft(self.__scaleSpinBox.value())
        else:
            self.__window.rotate_y_axis(-self.__rotation_spinbox.value())
        self.__updateViewframe()
    
    def __moveRight(self):
        selected_radio = self.__move_rotate_group.checkedButton()
        if selected_radio == self.__move_radio:
            self.__window.moveRight(self.__scaleSpinBox.value())
        else:
            self.__window.rotate_y_axis(self.__rotation_spinbox.value())
        self.__updateViewframe()

    def __moveUp(self):
        selected_radio = self.__move_rotate_group.checkedButton()

        if selected_radio == self.__move_radio:
            self.__window.moveUp(self.__scaleSpinBox.value())
        elif selected_radio == self.__rotate_radio:
            self.__window.rotate_x_axis(self.__rotation_spinbox.value())
        self.__updateViewframe()
    
    def __moveDown(self):
        selected_radio = self.__move_rotate_group.checkedButton()
        if selected_radio == self.__move_radio:
            self.__window.moveDown(self.__scaleSpinBox.value())
        else:
            self.__window.rotate_x_axis(-self.__rotation_spinbox.value())
        self.__updateViewframe()
    
    def __moveFront(self):
        self.__window.moveFront(self.__scaleSpinBox.value())
        self.__updateViewframe()

    def __moveBack(self):
        self.__window.moveBack(self.__scaleSpinBox.value())
        self.__updateViewframe()

    def __zoom(self, direction):
        if direction == "in":
            self.__window.zoomIn(self.__scaleSpinBox.value())
            self.__logs.logZoomIn(self.__scaleSpinBox.value())
        elif direction == "out":
            self.__window.zoomOut(self.__scaleSpinBox.value())
            self.__logs.logZoomOut(self.__scaleSpinBox.value())
        self.__updateViewframe()

    def __rotateLeft(self, angle):
        self.__window.rotate_z_axis(-angle)
        self.__updateViewframe() 

    def __rotateRight(self, angle):
        self.__window.rotate_z_axis(angle)
        self.__updateViewframe() 

    def __update_clipping_algorithm(self, radio_button):
        self.__clipping_algorithm = radio_button.algorithm
        self.__updateViewframe()

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
        transform_dialog = TransformObjectDialog(self.__display_file, self.__object_list, self.__window)
        transform_dialog.exec()
        self.__updateViewframe()

    def __exportFile(self):
        filename = QtWidgets.QFileDialog.getSaveFileName(caption="File to export", filter="Wavefront files (*.obj)")
        
        if filename[0] == '':
            return
        
        generator = GenerateOBJ(self.__display_file)
        generator.generateFileObj(filename[0])
    
    def __importFile(self):
        file_dialog = QtWidgets.QFileDialog()
        filepath = file_dialog.getOpenFileName(caption="Open Image", filter="Wavefront files (*.obj)")
        
        if filepath[0] == '':
            return

        reader =  ReaderOBJ()
        reader.openFile(filepath[0])
        
        for obj in reader.objects:
            self.__display_file.addObject(obj)
            if isinstance(obj, Point):
                self.__object_list.addItem(str(obj.name) + " (Ponto)")
            elif isinstance(obj, Line):
                self.__object_list.addItem(str(obj.name) + " (Reta)")
            elif isinstance(obj, Wireframe):
                self.__object_list.addItem(str(obj.name) + " (Polígono)")

        self.__updateViewframe()
    
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

    def __changeMoveRotate(self, button):
        if button == self.__move_radio:
            self.__back_button.setEnabled(True)
            self.__front_button.setEnabled(True)

            self.__back_button.show()
            self.__front_button.show()

            self.__left_button.setToolTip("Mover window para esquerda")
            self.__right_button.setToolTip("Mover window para direita")
            self.__up_button.setToolTip("Mover window para cima")
            self.__down_button.setToolTip("Mover window para baixo")
        else:
            self.__back_button.setEnabled(False)
            self.__front_button.setEnabled(False)
            self.__rotate_ccw_button.setEnabled(True)

            self.__back_button.hide()
            self.__front_button.hide()
            self.__rotate_ccw_button.show()

            self.__left_button.setToolTip("Rotacionar para esquerda no eixo y")
            self.__right_button.setToolTip("Rotacionar para direita no eixo y")
            self.__up_button.setToolTip("Rotacionar para cima no eixo x")
            self.__down_button.setToolTip("Rotacionar para baixo no eixo x")
        
    def __changeProjection(self):
        if self.__parallel_button.isChecked():
            self.__projection = Projection.PARALLEL
        else:
            self.__projection = Projection.PERSPECTIVE
        self.__updateViewframe()
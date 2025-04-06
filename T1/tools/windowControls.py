class WindowControls:
    def __init__(self, window, scale_spin_box, logs, update_viewframe):
        self.__window = window
        self.__scaleSpinBox = scale_spin_box
        self.__logs = logs
        self.__updateViewframe = update_viewframe

    def move_left(self):
        self.__move("left")
    
    def move_right(self):
        self.__move("right")
    
    def move_up(self):
        self.__move("up")
    
    def move_down(self):
        self.__move("down")
    
    def zoom_in(self):
        self.__zoom("in")
    
    def zoom_out(self):
        self.__zoom("out")
    
    def __move(self, direction):
        self.__window.move(direction, self.__scaleSpinBox.value())
        self.__logs.logWindowMovidaPara(direction, self.__scaleSpinBox.value())
        self.__updateViewframe()

    def __zoom(self, direction):
        if direction == "in":
            self.__window.zoomIn(self.__scaleSpinBox.value())
            self.__logs.logZoomIn(self.__scaleSpinBox.value())
        elif direction == "out":
            self.__window.zoomOut(self.__scaleSpinBox.value())
            self.__logs.logZoomOut(self.__scaleSpinBox.value())
        self.__updateViewframe()

    def rotate_window(self, angle):
        self.__window.rotate(angle)
        self.__logs.logWindowRotation(angle)
        self.__updateViewframe()
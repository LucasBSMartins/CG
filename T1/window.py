from setting import Settings

class Window:
    def __init__(self):
        # X e Y max e min da window
        self.__xw_min = Settings.windowXmin()
        self.__xw_max = Settings.windowXmax()
        self.__yw_min = Settings.windowYmin()
        self.__yw_max = Settings.windowYmax()
    
    @property
    def xw_min(self):
        return self.__xw_min
    
    @property
    def xw_max(self):
        return self.__xw_max
    
    @property
    def yw_min(self):
        return self.__yw_min
    
    @property
    def yw_max(self):
        return self.__yw_max
    
    def move(self, direction, scale):
        d_x = (self.__xw_max - self.__xw_min) * (scale / 100)
        d_y = (self.__yw_max - self.__yw_min) * (scale / 100)

        if direction == "left":
            self.__xw_max -= d_x
            self.__xw_min -= d_x
        elif direction == "right":
            self.__xw_max += d_x
            self.__xw_min += d_x
        elif direction == "up":
            self.__yw_max += d_y
            self.__yw_min += d_y
        elif direction == "down":
            self.__yw_max -= d_y
            self.__yw_min -= d_y

    def zoomIn(self, scale):
        scale = scale/100
        dx = ((self.__xw_max - self.__xw_min) * scale)/2
        dy = ((self.__yw_max - self.__yw_min) * scale)/2

        self.__xw_min += dx
        self.__xw_max -= dx
        self.__yw_min += dy
        self.__yw_max -= dy

    def zoomOut(self, scale):
        scale = scale/100
        dx = ((self.__xw_max - self.__xw_min) * scale)/2
        dy = ((self.__yw_max - self.__yw_min) * scale)/2

        self.__xw_min -= dx
        self.__xw_max += dx
        self.__yw_min -= dy
        self.__yw_max += dy
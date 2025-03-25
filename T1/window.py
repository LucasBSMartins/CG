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
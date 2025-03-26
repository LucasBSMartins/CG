class Settings():

    # Geometria da viewport
    @staticmethod
    def viewport():
        return (15, 20, 500, 420)
    
    # x min da viewport
    @staticmethod
    def viewportXmin():
        return Settings.viewport()[0]

    # x max da viewport
    @staticmethod
    def viewportXmax():
        return Settings.viewport()[0] + Settings.viewport()[2]

    # y min da viewport
    @staticmethod
    def viewportYmin():
        return Settings.viewport()[1]

    # y max da viewport
    @staticmethod
    def viewportYmax():
        return Settings.viewport()[1] + Settings.viewport()[3]
    
    @staticmethod
    def canvas():
        return( 250, 20, 530, 460)
    
        # x max inicial da window
    @staticmethod
    def windowXmax():
        return 1000
    
    # x min inicial da window
    @staticmethod
    def windowXmin():
        return -1000
    
    # y max inicial da window
    @staticmethod
    def windowYmax():
        return 1000
    
    # y min inicial da window
    @staticmethod
    def windowYmin():
        return -1000
    
    # Geometria do frame de ferramentas
    @staticmethod
    def menu_frame():
        return (20, 20, 220, 560)
    
    # Geometria do frame de objetos
    @staticmethod
    def objects_frame():
        return (10, 25, 200, 165)
    
    # Geometria do frame de botoes
    @staticmethod
    def buttons_frame():
        return (15, 190, 190, 60)   

    # Geometria do frame de controle
    @staticmethod
    def control_frame():
        return (15, 230, 190, 315)
    
    @staticmethod
    def backgroundColor():
        return "background-color: rgb(211,211,211)"

from enum import Enum
   
class Type(Enum):
    POINT = 1
    LINE = 2
    WIREFRAME = 3
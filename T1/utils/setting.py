class Settings():

    # Geometria da viewport
    @staticmethod
    def viewport():
        return (15, 15, 470, 400)
    
    @staticmethod
    def view_frame():
        return (250, 30, 530, 460)
    
    @staticmethod
    def canvas():
        return(15, 15, 500, 430)
    
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
      
    # Menor coordenada possível para x ou y do objeto
    @staticmethod
    def min_coord():
        return -1000000000
    
    # Maior coordenada possível para x ou y do objeto
    @staticmethod
    def max_coord():
        return 1000000000
    
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
        return (20, 30, 220, 560)
    
    # Geometria do frame de objetos
    @staticmethod
    def objects_frame():
        return (10, 35, 200, 165)
    
    # Geometria do frame de botoes
    @staticmethod
    def buttons_frame():
        return (15, 200, 190, 60)   

    # Geometria do frame de controle
    @staticmethod
    def control_frame():
        return (15, 240, 190, 250)
    
    # Geometria do frame de controle
    @staticmethod
    def clipping_frame():
        return (15, 500, 190, 50)
    
    
    @staticmethod
    def backgroundColor():
        return "background-color: rgb(211,211,211)"

    @staticmethod
    def menuStyleSheet():
        return """QMenu {
                background-color: rgb(240, 240, 240); /* Light background for the menu */
                border: none; /* Remove the outer border */
                margin: 2px;
            }

            QMenu::item {
                background-color: transparent;
                padding: 5px 20px;
                color: black;
            }

            QMenu::item:selected {
                background-color: rgb(170, 170, 170); /* Darker background on hover */
                color: white;
            }

            QMenu::separator {
                height: 1px;
                background: #c0c0c0; /* Color of the separator line */
                margin: 5px 0; /* Add some spacing above and below the line */
            }"""
    
    @staticmethod
    def menuButtonStyleSheet():
        return """
            QToolButton {
                background-color: rgb(211, 211, 211); /* Light gray background */
                color: black; /* Default text color */
                border: 1px solid #a1a1a1;
                border-radius: 2px;
                padding: 2px;
                font-size: 10px;
            }
            QToolButton::menu-indicator { image: none; }
            QToolButton:hover {
                background-color: rgb(100, 100, 100); /* Darker on hover */
                color: white; /* Change text color on hover */
                border: 1px solid #777777;
            }
            QToolButton:pressed {
                background-color: rgb(60, 60, 60); /* Even darker when pressed */
                color: white; /* Change text color on press */
            }
        """

from enum import Enum
   
class Type(Enum):
    POINT = 1
    LINE = 2
    WIREFRAME = 3

class RotationType(Enum):
    OBJECT_CENTER = "Centro do objeto"
    WORLD_CENTER = "Centro do mundo"
    ARBITRARY_POINT = "Ponto Arbitrário"

class ClippingAlgorithm(Enum):
    COHEN = "Método de Cohen Sutherland"
    LIANG = "Método de Liang-Barsky"
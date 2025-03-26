from utils.setting import Settings

class Window:
    def __init__(self):
        """Inicializa a janela com as coordenadas obtidas das configurações"""
        # Coordenadas iniciais da janela (mínimas e máximas para X e Y)
        # Valores obtidos da classe Settings
        self.__xw_min = Settings.windowXmin()  # X mínimo da window
        self.__xw_max = Settings.windowXmax()  # X máximo da window
        self.__yw_min = Settings.windowYmin()  # Y mínimo da window
        self.__yw_max = Settings.windowYmax()  # Y máximo da window
    
    # Propriedades para acesso seguro aos atributos privados
    @property
    def xw_min(self):
        """Retorna o valor mínimo do eixo X da window"""
        return self.__xw_min
    
    @property
    def xw_max(self):
        """Retorna o valor máximo do eixo X da window"""
        return self.__xw_max
    
    @property
    def yw_min(self):
        """Retorna o valor mínimo do eixo Y da window"""
        return self.__yw_min
    
    @property
    def yw_max(self):
        """Retorna o valor máximo do eixo Y da window"""
        return self.__yw_max
    
    def move(self, direction, scale):
        """
        Move a window na direção especificada
        
        Args:
            direction (str): Direção do movimento ('left', 'right', 'up', 'down')
            scale (float): Porcentagem do tamanho da window a ser movida
        """
        # Calcula o deslocamento baseado no tamanho atual da window
        d_x = (self.__xw_max - self.__xw_min) * (scale / 100)  # Deslocamento em X
        d_y = (self.__yw_max - self.__yw_min) * (scale / 100)  # Deslocamento em Y

        # Aplica o deslocamento conforme a direção
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
        """
        Aplica zoom para dentro (reduz a área visível)
        
        Args:
            scale (float): Porcentagem do zoom a ser aplicado
        """
        scale = scale/100  # Converte porcentagem para decimal
        # Calcula metade do delta para centralizar o zoom
        dx = ((self.__xw_max - self.__xw_min) * scale)/2  # Delta X
        dy = ((self.__yw_max - self.__yw_min) * scale)/2  # Delta Y

        # Reduz a window simetricamente em ambos os lados
        self.__xw_min += dx
        self.__xw_max -= dx
        self.__yw_min += dy
        self.__yw_max -= dy

    def zoomOut(self, scale):
        """
        Aplica zoom para fora (aumenta a área visível)
        
        Args:
            scale (float): Porcentagem do zoom a ser aplicado
        """
        scale = scale/100  # Converte porcentagem para decimal
        # Calcula metade do delta para centralizar o zoom
        dx = ((self.__xw_max - self.__xw_min) * scale)/2  # Delta X
        dy = ((self.__yw_max - self.__yw_min) * scale)/2  # Delta Y

        # Expande a window simetricamente em ambos os lados
        self.__xw_min -= dx
        self.__xw_max += dx
        self.__yw_min -= dy
        self.__yw_max += dy
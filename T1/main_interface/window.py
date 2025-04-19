from utils.setting import Settings
import numpy as np
from tools.matrixGenerator import MatrixGenerator

class Window:
    def __init__(self):
        """Inicializa a janela com as coordenadas obtidas das configurações"""
        # Coordenadas iniciais da janela (mínimas e máximas para X e Y)
        # Valores obtidos da classe Settings
        self.__xw_min = Settings.windowXmin()  # X mínimo da window
        self.__xw_max = Settings.windowXmax()  # X máximo da window
        self.__yw_min = Settings.windowYmin()  # Y mínimo da window
        self.__yw_max = Settings.windowYmax()  # Y máximo da window
       
        # Cantos da window
        self.__edges = [(self.__xw_min, self.__yw_min),
                         (self.__xw_max, self.__yw_min),
                         (self.__xw_min, self.__yw_max),
                         (self.__xw_max, self.__yw_max)]
        
        self.__xmin_scn = -1
        self.__xmax_scn = 1
        self.__ymin_scn = -1
        self.__ymax_scn = 1

        self.__view_up_vector = [0, 1]
    
    def move_direction(self, direction, scale):
        """
        Move a window na direção especificada
        
        Args:
            direction (str): Direção do movimento ('left', 'right', 'up', 'down')
            scale (float): Porcentagem do tamanho da window a ser movida
        """
        # Aplica o deslocamento conforme a direção
        if direction == "left":
            self.moveLeft(scale)
        elif direction == "right":
            self.moveRight(scale)
        elif direction == "up":
            self.moveUp(scale)
        elif direction == "down":
            self.moveDown(scale)

    # Movimentação para esquerda (sem rotação)
    def moveLeft(self, scale):
        distance = (self.__xw_max - self.__xw_min) * (scale/100000)
        self.__move(-distance, 0)

    # Movimentação para direita (sem rotação)
    def moveRight(self, scale):
        distance = (self.__xw_max - self.__xw_min) * (scale/100000)
        self.__move(distance, 0)

    # Movimentação para cima (sem rotação)
    def moveUp(self, scale):
        distance = (self.__yw_max - self.__yw_min) * (scale/100000)
        self.__move(0, distance)

    # Movimentação para baixo (sem rotação)
    def moveDown(self, scale):
        distance = (self.__yw_max - self.__yw_min) * (scale/100000)
        self.__move(0, -distance)

    # Rotação da window
    def rotate(self, theta):
        self.__view_up_vector = self.__rotatePoint(self.__view_up_vector, theta)
        self.__updateEdges(theta)
        
    # Função chamada por todas as movimentações para fazer a movimentação efetiva da window
    def __move(self, dx, dy):
        translation_matrix = MatrixGenerator.generateTranslationMatrix(dx, dy)
        new_edges = []
        for x, y in self.__edges:
            new_edge = np.matmul(np.array([x, y, 1]), translation_matrix)
            new_edges.append((new_edge[0], new_edge[1]))
        self.__edges = new_edges

    # Atualiza os cantos da window quando uma rotação acontece
    def __updateEdges(self, theta):
        (dx, dy) = self.__getCenter()
        translation_matrix1 = MatrixGenerator.generateTranslationMatrix(-dx, -dy)
        rotation_matrix = MatrixGenerator.generateRotationMatrix(theta)
        translation_matrix2 = MatrixGenerator.generateTranslationMatrix(dx, dy)
        transforming_matrix = np.matmul(translation_matrix1, np.matmul(rotation_matrix, translation_matrix2))

        new_edges = []
        for x, y in self.__edges:
            new_edge = np.matmul(np.array([x, y, 1]), transforming_matrix).tolist()[0:2]
            new_edges.append(new_edge)
        self.__edges = new_edges

    # Rotaciona um ponto por um ângulo
    def __rotatePoint(self, point, angle):
        rotation_matrix = MatrixGenerator.generateRotationMatrix(angle)
        result = np.matmul(np.array([point[0], point[1], 1]), rotation_matrix).tolist()[0:2]
        return result
    
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

    # Retorna o centro da window
    def __getCenter(self):
        x_cont = y_cont = 0
        for x, y in self.__edges:
            x_cont += x
            y_cont += y
        return (x_cont/4, y_cont/4)
    
    def windowNormalize(self):
        (Wxc, Wyc) = self.__getCenter()

        Sx = 2/(self.__xw_max - self.__xw_min)
        Sy = 2/(self.__yw_max - self.__yw_min)

        np_viewup = np.array(self.__view_up_vector)
        angle = np.degrees(np.arctan2(np_viewup[0], np_viewup[1]))

        translating_matrix = MatrixGenerator.generateTranslationMatrix(-Wxc, -Wyc)
        rotating_matrix = MatrixGenerator.generateRotationMatrix(-angle)
        scaling_matrix = MatrixGenerator.generateScalingMatrix(Sx, Sy)
        result = np.matmul(scaling_matrix, np.matmul(rotating_matrix, translating_matrix))
        return result.tolist()
    
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
    
    @property
    def view_up_vector(self):
        return self.__view_up_vector
        
    @property
    def xmin_scn(self):
        return self.__xmin_scn

    @property
    def xmax_scn(self):
        return self.__xmax_scn
    
    @property
    def ymin_scn(self):
        return self.__ymin_scn
    
    @property
    def ymax_scn(self):
        return self.__ymax_scn
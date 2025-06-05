from utils.setting import Settings
import numpy as np
from tools.matrixGenerator import MatrixGenerator

class Window:
    def __init__(self):
        """Inicializa a janela com as coordenadas obtidas das configurações"""
        self.__xmin_scn = -1
        self.__xmax_scn = 1
        self.__ymin_scn = -1
        self.__ymax_scn = 1

        self.__w_min = Settings.windowXmin()
        self.__w_max = Settings.windowXmax()
        self.__h_min = Settings.windowYmin()
        self.__h_max = Settings.windowYmax()

        self.__center = (0, 0, 0)
        self.__x_angle = 0
        self.__y_angle = 0
        self.__z_angle = 0
    
    def moveLeft(self, scale):
        distance = (self.__w_max - self.__w_min) * (scale/100)
        self.__move(-distance, 0, 0)

    def moveRight(self, scale):
        distance = (self.__w_max - self.__w_min) * (scale/100)
        self.__move(distance, 0, 0)

    def moveUp(self, scale):
        distance = (self.__w_max - self.__w_min) * (scale/100)
        self.__move(0, distance, 0)

    def moveDown(self, scale):
        distance = (self.__w_max - self.__w_min) * (scale/100)
        self.__move(0, -distance, 0)

    def moveFront(self, scale):
        distance = (self.__w_max - self.__w_min) * (scale/100)
        self.__move(0, 0, distance)

    def moveBack(self, scale):
        distance = (self.__w_max - self.__w_min) * (scale/100)
        self.__move(0, 0, -distance)

    def __move(self, dx, dy, dz):
        x = self.__center[0] + dx
        y = self.__center[1] + dy
        z = self.__center[2] + dz
        self.__center = (x, y, z)

    # Rotaciona a window no eixo z
    def rotate_z_axis(self, theta):
        self.__z_angle += theta

    # Rotaciona no eixo x
    def rotate_x_axis(self, theta):
        self.__x_angle += theta

    # Rotaciona no eixo y
    def rotate_y_axis(self, theta):
        self.__y_angle += theta
    
    def zoomIn(self, scale):
        scale = scale / 100
        dw = ((self.__w_max - self.__w_min) * scale) / 2
        dh = ((self.__h_max - self.__h_min) * scale) / 2

        self.__w_min += dw
        self.__w_max -= dw
        self.__h_min += dh
        self.__h_max -= dh

    def zoomOut(self, scale):
        scale = scale / 100
        dw = ((self.__w_max - self.__w_min) * scale) / 2
        dh = ((self.__h_max - self.__h_min) * scale) / 2

        self.__w_min -= dw
        self.__w_max += dw
        self.__h_min -= dh
        self.__h_max += dh
    
    def windowNormalize(self):
        (Wxc, Wyc, _) = self.__center

        Sx = 2 / (self.__w_max - self.__w_min)
        Sy = 2 / (self.__h_max - self.__h_min)

        rotating_matrix = MatrixGenerator.generateRotationMatrix(-self.__z_angle)
        scaling_matrix = MatrixGenerator.generateScalingMatrix(Sx, Sy)
        result = np.matmul(rotating_matrix, scaling_matrix)
        return result.tolist()

    # Retorna a matriz de projeção paralela ortogonal para projetar os objetos no espaço 3D
    def getParallelProjectionMatrix(self):
        vpr = self.__center
        translating_vpr = MatrixGenerator.generateTranslationMatrix3D(-vpr[0], -vpr[1], -vpr[2])
        rotating_x = MatrixGenerator.generateRotationMatrix3D_X(-self.__x_angle)
        rotating_y = MatrixGenerator.generateRotationMatrix3D_Y(-self.__y_angle)
        result = np.matmul(np.matmul(translating_vpr, rotating_x), rotating_y)
        return result
    
    # Prompt(s) empregado(s):
    #   - "Implemente o método `getPerspectiveProjectionMatrix` para uma classe que
    #     simula uma câmera ou janela de visualização. A função deve calcular a
    #     matriz de projeção em perspectiva.
    #     Deve considerar:
    #     - `self.__center` para a translação do VPR (View Plane Reference).
    #     - `self.__x_angle` e `self.__y_angle` para as rotações em X e Y.
    #     - Um fator de distância `d` (definido como 800) para a matriz de perspectiva.
    #     A função deve utilizar `MatrixGenerator.generateTranslationMatrix3D`,
    #     `MatrixGenerator.generateRotationMatrix3D_X`,
    #     `MatrixGenerator.generateRotationMatrix3D_Y` e `np.matmul` para combinar as matrizes
    #     na ordem correta: translação, rotação X, rotação Y e matriz de perspectiva."
    def getPerspectiveProjectionMatrix(self):
        vpr = self.__center
        
        # Gera a matriz de translação para mover o VPR para a origem
        translating_vpr = MatrixGenerator.generateTranslationMatrix3D(-vpr[0], -vpr[1], -vpr[2])
        
        # Gera as matrizes de rotação para alinhar o VPR com os eixos globais
        rotating_x = MatrixGenerator.generateRotationMatrix3D_X(-self.__x_angle)
        rotating_y = MatrixGenerator.generateRotationMatrix3D_Y(-self.__y_angle)

        # Fator de distância para a projeção em perspectiva (pode ser ajustado)
        d = 800

        # Matriz de projeção em perspectiva
        perspective_matrix = np.transpose(np.array([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 1/d, 0]
        ]))

        # Combina as matrizes na ordem correta: translação -> rotação X -> rotação Y -> perspectiva
        # A ordem das multiplicações de matrizes é crucial para o resultado final da projeção.
        result = np.matmul(np.matmul(np.matmul(translating_vpr, rotating_x), rotating_y), perspective_matrix)
        return result

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

    @property
    def x_angle(self):
        return self.__x_angle

    @property
    def y_angle(self):
        return self.__y_angle

    @property
    def z_angle(self):
        return self.__z_angle
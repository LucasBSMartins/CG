from abc import ABC, abstractmethod
import numpy as np
from tools.matrixGenerator import MatrixGenerator
from math import sqrt

class Object(ABC):
    # Classe abstrata de objeto, que será estendida no código 
    # para representação dos três tipos de objeto
    def __init__(self, name, tipo, coord, color="#000000"):
        self.__name = name
        self.__tipo = tipo
        self.__coord = coord
        self.__color = color

    @abstractmethod
    def draw(self, transformed_coord, painter):
        pass
    
    # Projeta e normaliza as coordenadas do objeto
    def projectAndNormalize(self, project, normalize):
        project_coords = []
        for x, y, z in self.coord:
            transformed_coord = (np.dot(np.array([x, y, z, 1]), np.array(project))).tolist()
            project_coords.append(transformed_coord[:2])
        normalize_coords = []
        for x, y in project_coords:
            transformed_coord = (np.dot(np.array([x, y, 1]), np.array(normalize))).tolist()
            normalize_coords.append(transformed_coord[:2])
        return normalize_coords

    # Translada o objeto
    def translate(self, dx, dy, dz):
        matrix = MatrixGenerator.generateTranslationMatrix3D(dx, dy, dz)
        self.__transform(matrix)

    # Escalona o objeto
    def scale(self, sx, sy, sz):
        center_coord = self.getCenter()

        translating = MatrixGenerator.generateTranslationMatrix3D(-center_coord[0], -center_coord[1], -center_coord[2])
        scaling = MatrixGenerator.generateScalingMatrix3D(sx, sy, sz)
        translating_back = MatrixGenerator.generateTranslationMatrix3D(center_coord[0], center_coord[1], center_coord[2])

        transforming_matrix = np.matmul(np.matmul(translating, scaling), translating_back)
        self.__transform(transforming_matrix)

    # Rotaciona o objeto em torno do eixo x
    def rotateXAxis(self, theta):
        matrix = MatrixGenerator.generateRotationMatrix3D_X(theta)
        self.__transform(matrix)

    # Rotaciona o objeto em torno do eixo y
    def rotateYAxis(self, theta):
        matrix = MatrixGenerator.generateRotationMatrix3D_Y(theta)
        self.__transform(matrix)

    # Rotaciona o objeto em torno do eixo z
    def rotateZAxis(self, theta):
        matrix = MatrixGenerator.generateRotationMatrix3D_Z(theta)
        self.__transform(matrix)

    # Rotaciona o objeto em torno de um eixo entre o centro do objeto e um ponto arbitrário
    def rotateArbitrary(self, theta, point):
        # Centro do objeto é um dos pontos do eixo
        center = self.getCenter()
        # Eixo
        axis = np.array([center[0] - point[0], center[1] - point[1], center[2] - point[2]])

        # Cos e sin dos angulos theta x e theta y
        v = sqrt(axis[1]**2 + axis[2]**2)
        cos_x = axis[2] / v
        sin_x = axis[1] / v
        l = sqrt(axis[0]**2 + v**2)
        cos_y = v/l
        sin_y = axis[0] / l

        # Translação para a origem
        translating = MatrixGenerator.generateTranslationMatrix3D(-center[0], -center[1], -center[2])
        # Rotação em torno do eixo x para trazer o eixo sobre o plano yz
        rotation_x = np.array([[1,   0,    0, 0],
                               [0,  cos_x, sin_x, 0],
                               [0,  -sin_x,  cos_x, 0],
                               [0,   0,    0, 1]])
        # Rotação em torno do eixo y para alinhar o eixo com o eixo z
        rotation_y = np.array([[ cos_y,  0, sin_y, 0],
                               [0,  1,   0, 0],
                               [-sin_y,  0, cos_y, 0],
                               [0,  0,   0, 1]])
        # Rotação em torno do eixo z com o angulo desejado
        rotation_z = MatrixGenerator.generateRotationMatrix3D_Z(theta)
        # Rotação de volta em torno do eixo y
        rotation_y_back = np.array([[ cos_y,  0, -sin_y, 0],
                               [0,  1,   0, 0],
                               [sin_y,  0, cos_y, 0],
                               [0,  0,   0, 1]])
        # Rotação de volta em torno do eixo x
        rotation_x_back = np.array([[1,   0,    0, 0],
                               [0,  cos_x, -sin_x, 0],
                               [0, sin_x,  cos_x, 0],
                               [0,   0,    0, 1]])
        # Translação de volta
        translating_back = MatrixGenerator.generateTranslationMatrix3D(center[0], center[1], center[2])

        # Matriz de transformação é o resultado da multiplicação de todas as matrizes
        transforming_matrix = translating @ rotation_x @ rotation_y @ rotation_z @ rotation_y_back @ rotation_x_back @ translating_back
        self.__transform(transforming_matrix)

    # Faz a transformação do objeto de acordo com uma matriz de transformação
    def __transform(self, matrix):
        new_coord = []
        for x, y, z in self.__coord:
            new = np.matmul(np.array([x, y, z, 1]), matrix).tolist()
            new_coord.append((new[0], new[1], new[2]))
        self.__coord = new_coord

    @property
    def name(self):
        return self.__name
    
    @property
    def coord(self):
        return self.__coord
    
    @property
    def tipo(self):
        return self.__tipo

    @coord.setter
    def coord(self, new_coord):
        self.__coord = new_coord

    @name.setter
    def name(self, new_name):
        self.__name = new_name

    @property
    def color(self):
        return self.__color

    @color.setter
    def color(self, color):
        self.__color = color

    def getCenter(self):
        coord_len = len(self.__coord)
        center_x = center_y = center_z = 0
        for x, y, z in self.__coord:
            center_x += x / coord_len
            center_y += y / coord_len
            center_z += z / coord_len
        return (center_x, center_y, center_z)
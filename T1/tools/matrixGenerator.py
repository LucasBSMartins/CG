import numpy as np

class MatrixGenerator:
    @staticmethod
    def generateScalingMatrix(sx, sy):
        return np.array([[sx, 0, 0],
                         [0, sy, 0],
                         [0, 0,  1]])
    
    @staticmethod
    def generateTranslationMatrix(dx, dy):
        return np.array([[ 1,  0, 0],
                         [ 0,  1, 0],
                         [dx, dy, 1]])
    @staticmethod
    def generateRotationMatrix(theta):
        angle = np.radians(theta)
        cos = np.cos(angle)
        sin = np.sin(angle)
        return np.array([[cos, -sin, 0],
                         [sin,  cos, 0],
                         [  0,    0, 1]])

    # Matriz de escala 3D
    @staticmethod
    def generateScalingMatrix3D(sx, sy, sz):
        return np.array([[sx,  0,  0, 0],
                         [ 0, sy,  0, 0],
                         [ 0,  0, sz, 0],
                         [ 0,  0,  0, 1]])

    # Matriz de translação 3D
    @staticmethod
    def generateTranslationMatrix3D(dx, dy, dz):
        return np.array([[ 1,  0,  0, 0],
                         [ 0,  1,  0, 0],
                         [ 0,  0,  1, 0],
                         [dx, dy, dz, 1]])

    # Matriz de rotação 3D ao redor do eixo X
    @staticmethod
    def generateRotationMatrix3D_X(theta):
        angle = np.radians(theta)
        cos = np.cos(angle)
        sin = np.sin(angle)
        return np.array([[1,   0,    0, 0],
                         [0,  cos, sin, 0],
                         [0,  -sin,  cos, 0],
                         [0,   0,    0, 1]])

    # Matriz de rotação 3D ao redor do eixo Y
    @staticmethod
    def generateRotationMatrix3D_Y(theta):
        angle = np.radians(theta)
        cos = np.cos(angle)
        sin = np.sin(angle)
        return np.array([[ cos,  0, -sin, 0],
                         [   0,  1,   0, 0],
                         [sin,  0, cos, 0],
                         [   0,  0,   0, 1]])

    # Matriz de rotação 3D ao redor do eixo Z
    @staticmethod
    def generateRotationMatrix3D_Z(theta):
        angle = np.radians(theta)
        cos = np.cos(angle)
        sin = np.sin(angle)
        return np.array([[cos, sin, 0, 0],
                         [-sin,  cos, 0, 0],
                         [  0,    0, 1, 0],
                         [  0,    0, 0, 1]])
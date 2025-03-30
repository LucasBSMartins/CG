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

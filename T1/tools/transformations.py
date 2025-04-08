import numpy as np
from tools.matrixGenerator import MatrixGenerator as MG

class Transformations:
    def __init__(self, window=None):
        self.__mg = MG()
        if window:
            self.__window = window

    def translation(self, objeto, dx, dy):
        np_viewup = np.array(self.__window.view_up_vector)
        angle = np.degrees(np.arctan2(np_viewup[0], np_viewup[1]))

        rotation = self.__mg.generateRotationMatrix(-angle)
        translating_matrix = self.__mg.generateTranslationMatrix(dx, dy)
        rotation_back = self.__mg.generateRotationMatrix(angle)
        matriz_reposicionamento = np.matmul(np.matmul(rotation, translating_matrix), rotation_back)
        return self._apply_transformation(objeto, matriz_reposicionamento)
    
    def rotateAroundObjectCenter(self, objeto, theta):
        center_coord = objeto.getCenter()

        translating = self.__mg.generateTranslationMatrix(-center_coord[0], -center_coord[1])
        rotation_matrix = self.__mg.generateRotationMatrix(theta)
        translating_back = self.__mg.generateTranslationMatrix(center_coord[0], center_coord[1])
        
        matriz_reposicionamento = np.matmul(np.matmul(translating, rotation_matrix), translating_back)
        return self._apply_transformation(objeto, matriz_reposicionamento)
    
    # Faz a rotação do objeto em torno do centro do mundo
    def rotateAroundWorldCenter(self, objeto, theta):
        matriz_reposicionamento = self.__mg.generateRotationMatrix(theta)
        return self._apply_transformation(objeto, matriz_reposicionamento)

    # Faz a rotação do objeto em torno de um ponto arbitrário
    def rotateAroundArbitraryPoint(self, objeto, theta, coord):
        translating = self.__mg.generateTranslationMatrix(-coord[0], -coord[1])
        rotation_matrix = self.__mg.generateRotationMatrix(theta)
        translating_back = self.__mg.generateTranslationMatrix(coord[0], coord[1])

        matriz_reposicionamento = np.matmul(np.matmul(translating, rotation_matrix), translating_back)
        return self._apply_transformation(objeto, matriz_reposicionamento)

    def scaling(self, objeto, sx, sy):
        center_coord = objeto.getCenter()

        translating = self.__mg.generateTranslationMatrix(-center_coord[0], -center_coord[1])
        scaling = self.__mg.generateScalingMatrix(sx, sy)
        translating_back = self.__mg.generateTranslationMatrix(center_coord[0], center_coord[1])

        matriz_reposicionamento = np.matmul(np.matmul(translating, scaling), translating_back)
        return self._apply_transformation(objeto, matriz_reposicionamento)

    def _apply_transformation(self, objeto, transformation_matrix):
        new_coord = []
        for x, y in objeto.coord:
            new = np.matmul(np.array([x, y, 1]), transformation_matrix).tolist()
            new_coord.append([new[0], new[1]])
        return new_coord
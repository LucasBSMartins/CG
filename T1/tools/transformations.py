from math import cos, sin
from tools.matrixGenerator import MatrixGenerator as MG

class Transformations():
    def __init__(self):
        self.__mg = MG()

    def translation(self, base, dx, dy):
        
        resultante = [[0, 0, 0]]

        matriz_reposicionamento = self.__mg.generateTranslationMatrix(dx, dy)

        for i in range(len(base)):
            # Iterando nas colunas da matriz de transformação
            for j in range(len(matriz_reposicionamento[0])):

                for k in range(len(matriz_reposicionamento)):
                    resultante[i][j] += base[i][k] * matriz_reposicionamento[k][j]

        return resultante

    def rotation(self, base, coef_rotacao):
        
        resultante = [[0, 0, 0]]

        matriz_reposicionamento = self.__mg.generateTranslationMatrix(coef_rotacao)

        for i in range(len(base)):
            # Iterando nas colunas da matriz de transformação
            for j in range(len(matriz_reposicionamento[0])):

                for k in range(len(matriz_reposicionamento)):
                    resultante[i][j] += base[i][k] * matriz_reposicionamento[k][j]

        return resultante

    def scaling (self, base, sx, sy):

        resultante = [[0, 0, 0]]

        # Escalonamento representa o S0 e S1 da matriz passada em aula
        matriz_reposicionamento = self.__mg.generateTranslationMatrix(sx, sy)

        for i in range(len(base)):
            # Iterando nas colunas da matriz de transformação
            for j in range(len(matriz_reposicionamento[0])):

                for k in range(len(matriz_reposicionamento)):
                    resultante[i][j] += base[i][k] * matriz_reposicionamento[k][j]

        return resultante
    
    def transformacao_resultante(self, reposicionamento):

        result = [[0, 0, 0]]
        # Iterando nas coordenadas do objeto
        for i in range(len(self.coord)):
            # Iterando nas colunas da matriz de transformação
            for j in range(len(reposicionamento[0])):

                for k in range(len(reposicionamento)):
                    result[i][j] += self.coord[i][k] * reposicionamento[k][j]

        return result

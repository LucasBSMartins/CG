from abc import ABC, abstractmethod
from math import sin, cos

class Object(ABC):
    # Classe abstrata de objeto, que será estendida no código 
    # para representação dos três tipos de objeto
    def __init__(self, name, tipo, coord):
        self.__name = name
        self.__tipo = tipo
        self.__coord = coord

    @abstractmethod
    def draw(self, transformed_coord, painter):
        pass

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


    """
    Método usado para cálculo da matriz resultante
    """
    @property
    def transformacao_resultante(self, reposicionamento):

        result = [[0, 0, 0]]
        # Iterando nas coordenadas do objeto
        for i in range(len(self.coord)):
                # Iterando nas colunas da matriz de transformação
            for j in range(len(reposicionamento[0])):

                for k in range(len(reposicionamento)):
                    result[i][j] += self.coord[i][k] * reposicionamento[k][j]

        # Printando coordenadas reposicionadas
        for r in result:
            print(r)

        return result



    """
    Métodos abaixo para realizar o calculo da matriz resultante de transformação
    """
    def translacao(self, base, deslocamento):
        resultante = [[0, 0, 0]]

        # Deslocamento representa o Dx e Dy da matriz de translaçao passada em aula
        matriz_reposicionamento = [[1, 0, 0],
                                    [0, 1, 0],
                                    [deslocamento[0], deslocamento[1], 1]]

        for i in range(len(base)):
                # Iterando nas colunas da matriz de transformação
            for j in range(len(matriz_reposicionamento[0])):

                for k in range(len(matriz_reposicionamento)):
                    resultante[i][j] += base[i][k] * matriz_reposicionamento[k][j]

        return resultante

    def escalonamento(self, base, escalonamento):

        resultante = [[0, 0, 0]]

        # Escalonamento representa o S0 e S1 da matriz passada em aula
        matriz_reposicionamento = [[escalonamento[0], 0, 0],
                                    [0, escalonamento[1], 0],
                                    [0, 0, 1]]

        for i in range(len(base)):
                # Iterando nas colunas da matriz de transformação
            for j in range(len(matriz_reposicionamento[0])):

                for k in range(len(matriz_reposicionamento)):
                    resultante[i][j] += base[i][k] * matriz_reposicionamento[k][j]

        return resultante

    def rotacao(self, base, coef_rotacao):
        
        resultante = [[0, 0, 0]]

        # Escalonamento representa o S0 e S1 da matriz passada em aula
        matriz_reposicionamento = [[cos(coef_rotacao), -sin(coef_rotacao), 0],
                                    [sin(coef_rotacao), cos(coef_rotacao), 0],
                                    [0, 0, 1]]

        for i in range(len(base)):
                # Iterando nas colunas da matriz de transformação
            for j in range(len(matriz_reposicionamento[0])):

                for k in range(len(matriz_reposicionamento)):
                    resultante[i][j] += base[i][k] * matriz_reposicionamento[k][j]

        return resultante

from utils.setting import Type, ClippingAlgorithm

class Clipping:
    # Chama o clipping de acordo com o tipo do objeto
    @staticmethod
    def clip(obj, coords, window, algorithm):
        if obj.tipo == Type.POINT:
            return Clipping.pointClipping(coords, window)
        elif obj.tipo == Type.LINE:
            if algorithm == ClippingAlgorithm.COHEN:
                return Clipping.cohenSutherland(coords, window)
            else:
                return Clipping.liangBarsky(coords, window)
        elif obj.tipo == Type.WIREFRAME:
            return Clipping.sutherlandHodgeman(coords, window)
    
    # Clipping de pontos
    @staticmethod
    def pointClipping(coords, window):
        if window.xmin_scn <= coords[0][0] <= window.xmax_scn and window.ymin_scn <= coords[0][1] <= window.ymax_scn:
            return (True, coords)
        else:
            return (False, coords)
    
    # Clipping de linhas - Cohen Sutherland
    @staticmethod
    def cohenSutherland(coords, window):
        # Pontos (x1, y1) e (x2, y2) da linha
        x1 = coords[0][0]
        y1 = coords[0][1]
        x2 = coords[1][0]
        y2 = coords[1][1]
        code1 = Clipping.CSRegionCode(x1, y1, window)
        code2 = Clipping.CSRegionCode(x2, y2, window)

        # O loop vai ajustando os pontos da linha de acordo com as intersecções com os limites
        # da window até que a linha esteja completamente dentro ou completamente fora da janela
        while True:
            # Os 2 pontos estão dentro da window (linha completamente contida na janela)
            if code1 == code2 == 0b0000:
                return (True, [[x1, y1], [x2, y2]])
            # Linha completamente fora da janela
            elif (code1 & code2) != 0b0000:
                return (False, coords)
            # Linha parciamente contida na janela
            else:
                # out é o código do ponto (ou de um dos pontos) que está fora da janela
                if code1 != 0b0000:
                    out = code1
                else:
                    out = code2
                # Intersecção do ponto com a borda esquerda da janela
                if out & 0b0001:
                    m = (y2 - y1)/(x2 - x1)
                    x = window.xmin_scn
                    y = m * (x - x1) + y1
                # Intersecção do ponto com a borda direita da janela
                elif out & 0b0010:
                    m = (y2 - y1)/(x2 - x1)
                    x = window.xmax_scn
                    y = m * (x - x1) + y1
                # Intersecção do ponto com a borda fundo da janela
                elif out & 0b0100:
                    m = (x2 - x1)/(y2 - y1)
                    y = window.ymin_scn
                    x = x1 + m * (y - y1)
                # Intersecção do ponto com a borda topo da janela
                elif out & 0b1000:
                    m = (x2 - x1)/(y2 - y1)
                    y = window.ymax_scn
                    x = x1 + m * (y - y1)
                
                # Substitui ponto fora da janela (ponto do código out) pela intersecção
                if out == code1:
                    x1 = x
                    y1 = y
                    code1 = Clipping.CSRegionCode(x1, y1, window)
                else:
                    x2 = x
                    y2 = y
                    code2 = Clipping.CSRegionCode(x2, y2, window)

    # Determina o código de região de um ponto (x, y) - usado no algoritmo de Cohen Sutherland
    @staticmethod
    def CSRegionCode(x, y, window):
        code = 0b0000
        if x < window.xmin_scn:
            code |= 0b0001
        elif x > window.xmax_scn:
            code |= 0b0010
        if y < window.ymin_scn:
            code |= 0b0100
        elif y > window.ymax_scn:
            code |= 0b1000
        return code
    
    # Clipping de linhas - Liang-Barsky
    @staticmethod
    def liangBarsky(coords, window):
        # Pontos (x1, y1) e (x2, y2) da linha
        x1 = coords[0][0]
        y1 = coords[0][1]
        x2 = coords[1][0]
        y2 = coords[1][1]

        # p1 p2 p3 p4
        p = [-(x2 - x1), x2 - x1, -(y2 - y1), y2 - y1]
        # q1 q2 q3 q4
        q = [x1 - window.xmin_scn, window.xmax_scn - x1, y1 - window.ymin_scn, window.ymax_scn - y1]

        fora_dentro = 0
        dentro_fora = 1

        for idx, pk in enumerate(p):
            # Pararela a um dos limites e fora dos limites
            if pk == 0 and q[idx] < 0:
                return (False, coords)
            # Linha vem de fora para dentro
            elif pk < 0:
                r = q[idx]/pk
                fora_dentro = max(fora_dentro, r)
            # Linha vem de dentro para fora
            elif pk > 0:
                r = q[idx]/pk
                dentro_fora = min(dentro_fora, r)

        # Linha completamente fora
        if fora_dentro > dentro_fora:
            return (False, coords)
        
        # Calcular pontos da linha clipada
        new_x1 = x1 + fora_dentro*(x2-x1)
        new_y1 = y1 + fora_dentro*(y2-y1)
        new_x2 = x1 + dentro_fora*(x2-x1)
        new_y2 = y1 + dentro_fora*(y2-y1)
        return (True, [[new_x1, new_y1], [new_x2, new_y2]])
    
    # Clipping de polígonos - Sutherland Hodgeman
    @staticmethod
    def sutherlandHodgeman(coords, window):
        # Cantos da window
        clipping_window = [[window.xmin_scn, window.ymin_scn],
                       [window.xmin_scn, window.ymax_scn],
                       [window.xmax_scn, window.ymax_scn],
                       [window.xmax_scn, window.ymin_scn]]

        clipped_coords = coords

        # Percorre os cantos da window em sentido horário
        for i in range(len(clipping_window)):
            previous_coords = clipped_coords
            clipped_coords = []

            # window_edge1 e window_edge2 formam a borda da window usada para recortar o polígono
            window_edge1 = clipping_window[i]
            window_edge2 = clipping_window[(i+1)%len(clipping_window)]

            # Percorre os pontos (clipados pela borda anterior da window) do polígono
            for j in range(len(previous_coords)):
                # current_point e next_point formam uma aresta do polígono
                current_point = previous_coords[j]
                next_point = previous_coords[(j+1)%len(previous_coords)]

                current_inside = Clipping.SHInside(current_point, window_edge1, window_edge2)
                next_inside = Clipping.SHInside(next_point, window_edge1, window_edge2)
                
                # next_point dentro da window
                if next_inside:
                    # current_point fora da window
                    if not current_inside:
                        clipped_coords.append(Clipping.SHIntersection(current_point, next_point, window_edge1, window_edge2))
                    clipped_coords.append(next_point)
                # next_point fora da window e current_point dentro da window
                elif current_inside:
                    clipped_coords.append(Clipping.SHIntersection(current_point, next_point, window_edge1, window_edge2))

        if len(clipped_coords) == 0:
            return (False, coords)
        else:
            return (True, clipped_coords)
    
    # Determina se um ponto está a direita de um vetor (aresta da window) - usado no algoritmo de Sutherland Hodgeman
    # Se o ponto estiver a direita desse vetor, ele está dentro da window
    @staticmethod
    def SHInside(point, edge1, edge2):
            return ((edge2[0]-edge1[0]) * (point[1]-edge1[1])) < ((edge2[1]-edge1[1]) * (point[0]-edge1[0]))

    # Determina a interseção de 2 retas
    @staticmethod
    def SHIntersection(point1, point2, edge1, edge2):
        numx = (edge1[0]*edge2[1] - edge1[1]*edge2[0])*(point1[0]-point2[0]) - (edge1[0]-edge2[0])*(point1[0]*point2[1]-point1[1]*point2[0])
        den = (edge1[0]-edge2[0])*(point1[1]-point2[1]) - (edge1[1]-edge2[1])*(point1[0]-point2[0])
        numy = (edge1[0]*edge2[1] - edge1[1]*edge2[0])*(point1[1]-point2[1]) - (edge1[1]-edge2[1])*(point1[0]*point2[1]-point1[1]*point2[0])
        return (numx/den, numy/den)
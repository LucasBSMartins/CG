from objects.point import Point
from objects.line import Line
from objects.wireframe import Wireframe
from PySide6.QtGui import QColor
import os

class ReaderOBJ:
    def __init__(self):
        self.objects = []

    def openFile(self, name_file):
        vertices, graphics = self.__read_obj_file(name_file)
        self.__create_graphics_elements(graphics, vertices)

    def __create_graphics_elements(self, graphics_elements, vertices):
        for name, data in graphics_elements.items():
            color = data["color"]
            points = []
            lines = [] # Lista para armazenar os pares de pontos que formam as arestas
            for part in data["parts"]:
                obj_type = part["type"]
                indices = part["indices"]
                # Get the vertex coordinates from the indices
                for i in range(0, len(indices) - 1, 1): # Iterar sobre os índices para criar pares de pontos
                    if indices[i] > 0 and indices[i] <= len(vertices) and indices[i+1] > 0 and indices[i+1] <= len(vertices):
                        points.append(vertices[indices[i]-1])
                        points.append(vertices[indices[i+1]-1])
                        lines.append((vertices[indices[i]-1], vertices[indices[i+1]-1])) # Adiciona o par de pontos à lista de arestas
                    else:
                        print(f"Warning: Invalid vertex index in object {name}, skipping.")
                element = None
            if obj_type == "p":
                element = Point(name.strip(), points, color)
            elif obj_type == "l":
                element = Line(name.strip(), points, color) # Passa a lista completa de pontos para a linha
            elif obj_type == "f":
                element = Wireframe(name.strip(), points, color) # Assuming Wireframe handles faces
            elif obj_type == "OBJECT_3D":
                element = Wireframe(name.strip(), points, color)

            if element:
                self.objects.append(element)

    def __get_edges_from_indices(self, indices, edges):
        # Adicionado lógica para verificar se o tamanho da coordenada é 2, se for adiciona 0.0.
        return [(edges[i - 1][0], edges[i - 1][1], 0.0) if len(edges[i-1]) == 2 else (edges[i - 1][0], edges[i-1][1], 0.0) if len(edges[i-1]) == 2  else edges[i - 1] for i in indices]

    def __read_mtl_file(self, name_file: str) -> dict:
        colors = {}
        try:
            with open(name_file, "r") as file:
                for line in file:
                    words = line.strip().split()
                    if words and words[0] == "Kd":
                        try:
                            r = float(words[1])
                            g = float(words[2])
                            b = float(words[3])
                            colors[name] = QColor.fromRgbF(r, g, b, 1.0)
                        except (ValueError, IndexError):
                            print(f"Warning: Invalid Kd values in MTL file: {line.strip()}")
                    elif words and words[0] == "newmtl":
                        name = words[1]
        except FileNotFoundError:
            print(f"Warning: MTL file not found at {name_file}")
        return colors

    def __read_obj_file(self, name_file: str) -> tuple:
        vertices = []
        graphics = {}
        colors = {}
        current_object_name = None
        color_obj = None  # Initialize color_obj here

        with open(name_file, "r") as file:
            for line in file:
                words = line.strip().split()
                if not words:
                    continue

                if words[0] == "mtllib":
                    mtl_filename = words[1].strip()
                    mtl_path_wavefront = os.path.join("wavefront", mtl_filename)
                    colors = self.__read_mtl_file(mtl_path_wavefront)
                elif words[0] == "usemtl":
                    color_obj = colors.get(words[1])
                elif words[0] == "v":
                    # Na leitura dos vértices (elif words[0] == "v":), o código agora verifica o número de componentes.
                    # Se houver 3 componentes, ele cria uma tupla (x, y, z).
                    # Se houver 2 componentes, ele cria uma tupla (x, y, 0.0), efetivamente adicionando uma coordenada z de 0.
                    if len(words) == 4:
                        vertex_coords = tuple(float(w) for w in words[1:4])
                    elif len(words) == 3:
                        vertex_coords = tuple(float(w) for w in words[1:3]) + (0.0,)  # Adiciona z=0.0
                    vertices.append(vertex_coords)
                elif words[0] == "o":
                    current_object_name = words[1]
                    graphics[current_object_name] = {"color": color_obj, "parts": []} # Store color here
                elif words[0] in ("p", "l", "f"):
                    if current_object_name:
                        try:
                            indices = [int(w) for w in words[1:]]
                            if current_object_name not in graphics:
                                graphics[current_object_name] = {"color": color_obj, "parts": []}
                            graphics[current_object_name]["parts"].append({
                                "type": words[0],
                                "indices": indices,
                            })
                        except ValueError:
                            print(f"Warning: Invalid vertex index in OBJ file: {line.strip()}")
                    else:
                        print(f"Warning: Geometry type '{words[0]}' encountered before object name. Skipping.")
        return vertices, graphics
    
    def __read_tuple(self, words: list) -> tuple:
        return tuple(float(w) for w in words[1:4])

    def __read_list(self, words: list) -> list:
        return [int(w) for w in words]

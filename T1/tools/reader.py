from objects.point import Point
from objects.line import Line
from objects.wireframe import Wireframe
from PySide6.QtGui import QColor
import os 

class ReaderOBJ:
    def __init__(self):
        self.objects = []

    def openFile(self, name_file):
        edges, graphics = self.__read_obj_file(name_file)
        self.__create_graphics_elements(graphics, edges)

    def __create_graphics_elements(self, graphics_elements, edges):
        for name, data in graphics_elements.items():
            obj_type, color, indices, *fill = data
            element = None
            points = self.__get_edges_from_indices(indices, edges)

            if obj_type == "Ponto":
                element = Point(name.strip(), points, color)
            elif obj_type == "Reta":
                element = Line(name.strip(), points, color)
            elif obj_type == "Wireframe":
                element = Wireframe(name.strip(), points, color)

            if element:
                self.objects.append(element)

    def __get_edges_from_indices(self, indices, edges):
        return [(edges[i - 1][0], edges[i - 1][1]) for i in indices]

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
        edges = []
        graphics = {}
        colors = {}
        name_obj = ""
        type_obj = ""
        color_obj = ""
        points = []

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
                    edges.append(self.__read_tuple(words))
                elif words[0] == "o":
                    name_obj = words[1]
                elif words[0] == "p":
                    type_obj = "Ponto"
                    points = [int(words[1])]
                    graphics[name_obj] = [type_obj, color_obj, points]
                elif words[0] == "l":
                    type_obj = "Reta" if len(words) == 3 else "Wireframe"
                    points = self.__read_list(words[1:])
                    graphics[name_obj] = [type_obj, color_obj, points, False] if type_obj == "Wireframe" else [type_obj, color_obj, points]
                elif words[0] == "f":
                    type_obj = "Wireframe"
                    points = self.__read_list(words[1:])
                    graphics[name_obj] = [type_obj, color_obj, points, True]

        return edges, graphics

    def __read_tuple(self, words: list) -> tuple:
        return tuple(float(w) for w in words[1:4])

    def __read_list(self, words: list) -> list:
        return [int(w) for w in words]
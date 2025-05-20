from objects.point import Point
from objects.line import Line
from objects.wireframe import Wireframe
from utils.setting import Type
from PySide6.QtGui import QColor
import os

class GenerateOBJ:
    def __init__(self, display_file):
        self.objects = {}
        self.vertices = []
        self.colors = {}
        self._generate_data(display_file)

    def _generate_data(self, display_file):
        for obj in display_file.objects_list:
            obj_data = {"color": obj.color, "parts": []}
            if obj.tipo == Type.POINT:
                for coord in obj.coord:
                    vertex_idx = self._get_vertex_index(coord)
                    obj_data["parts"].append({"type": "p", "indices": [vertex_idx]})
                self.objects[obj.name] = obj_data
            elif obj.tipo == Type.WIREFRAME:
                indices = []
                for coord in obj.coord:
                    vertex_idx = self._get_vertex_index(coord)
                    indices.append(vertex_idx)
                obj_data["parts"].append({"type": "f", "indices": indices})
                self.objects[obj.name] = obj_data
            elif obj.tipo == Type.LINE:
                if len(obj.coord) % 2 != 0:
                    print(f"Warning: Line object {obj.name} has an odd number of coordinates. Skipping last coordinate.")
                for i in range(0, len(obj.coord), 2):
                    v1_idx = self._get_vertex_index(obj.coord[i])
                    v2_idx = self._get_vertex_index(obj.coord[i+1])
                    obj_data["parts"].append({"type": "l", "indices": [v1_idx, v2_idx]})
                self.objects[obj.name] = obj_data
            elif obj.tipo == Type.OBJECT_3D:
                # Agrupa os pontos em arestas para o formato OBJ
                if len(obj.coord) % 2 != 0:
                    print(f"Warning: 3D object {obj.name} has an odd number of coordinates. Skipping last coordinate.")
                for i in range(0, len(obj.coord), 2):
                    v1_idx = self._get_vertex_index(obj.coord[i])
                    v2_idx = self._get_vertex_index(obj.coord[i+1])
                    obj_data["parts"].append({"type": "l", "indices": [v1_idx, v2_idx]})
                self.objects[obj.name] = obj_data
            else:
                print(f"Warning: Unknown object type for {obj.name}: {obj.tipo}")
                indices = []
                for coord in obj.coord:
                    vertex_idx = self._get_vertex_index(coord)
                    indices.append(vertex_idx)
                obj_data["parts"].append({"type": "l", "indices": indices})
                self.objects[obj.name] = obj_data

    def _get_vertex_index(self, coord):
        if coord not in self.vertices:
            self.vertices.append(coord)
        return self.vertices.index(coord) + 1

    def generateFileObj(self, name_file):
        mtl_filename = "cores.mtl"
        mtl_filepath = os.path.join("wavefront", mtl_filename)
        wavefront_dir = os.path.dirname(mtl_filepath)
        if not os.path.exists(wavefront_dir):
            os.makedirs(wavefront_dir)

        with open(mtl_filepath, "w") as mtl_file:
            mtl_file.write("")
        with open(name_file, "w") as obj_file:
            # Escreve os vértices (v)
            for i, vertex in enumerate(self.vertices):
                if len(vertex) == 2:
                    obj_file.write(f"v {vertex[0]:.6f} {vertex[1]:.6f} 0.0\n")
                elif len(vertex) == 3:
                    obj_file.write(f"v {vertex[0]:.6f} {vertex[1]:.6f} {vertex[2]:.6f}\n")
                else:
                    print(f"Warning: Unexpected vertex format: {vertex}. Writing with 0.0 for Z.")
                    obj_file.write(f"v {vertex[0]:.6f} {vertex[1]:.6f} 0.0\n")

            obj_file.write(f"mtllib {mtl_filename}\n\n")

            # Escreve os objetos (o) e seus componentes
            for name, data in self.objects.items():
                obj_file.write(f"o {name}\n")  # Nome do objeto
                mtl_use = self._generateMTLFile(data["color"])
                obj_file.write(mtl_use)
                for part in data["parts"]:
                    obj_file.write(f"{part['type']} {' '.join(map(str, part['indices']))}\n")  # tipo (l, f, p) e índices

    def _generateMTLFile(self, color_data) -> str:
        if isinstance(color_data, str):
            try:
                r_str, g_str, b_str = color_data.split(',')
                r = int(r_str.strip())
                g = int(g_str.strip())
                b = int(b_str.strip())
                qcolor = QColor(r, g, b)
                return self.__process_qcolor_for_mtl(qcolor)
            except ValueError:
                print(f"Warning: Invalid color string format: {color_data}. Using Default.")
                return "usemtl Default\n"
        elif isinstance(color_data, QColor):
            return self.__process_qcolor_for_mtl(color_data)
        else:
            print(f"Warning: Unexpected color data type: {type(color_data)}. Using Default.")
            return "usemtl Default\n"

    def __process_qcolor_for_mtl(self, qcolor: QColor) -> str:
        r_float, g_float, b_float, _ = qcolor.getRgbF()
        r_kd, g_kd, b_kd = r_float, g_float, b_float
        rgb_tuple_0_255 = (int(r_float * 255), int(g_float * 255), int(b_float * 255))
        color_id = self.colors.setdefault(rgb_tuple_0_255, len(self.colors) + 1)
        color_name = f"Cor_{color_id}"
        mtl_filename = "cores.mtl"
        mtl_filepath = os.path.join("wavefront", mtl_filename)
        if not hasattr(self, 'written_mtl_colors'):
            self.written_mtl_colors = set()
        if rgb_tuple_0_255 not in self.written_mtl_colors:
            with open(mtl_filepath, "a") as mtl_file:
                mtl_file.write(f"newmtl {color_name}\n")
                mtl_file.write(f"Kd {r_kd:.6f} {g_kd:.6f} {b_kd:.6f}\n\n")
            self.written_mtl_colors.add(rgb_tuple_0_255)
        return f"usemtl {color_name}\n"

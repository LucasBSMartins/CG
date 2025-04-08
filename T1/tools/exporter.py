from utils.setting import Type
from PySide6.QtGui import QColor
import os

class GenerateOBJ:
    def __init__(self, display_file):
        self.objects = {}
        self.edges = []
        self.colors = {}
        self._generate_data(display_file)

    def _generate_data(self, display_file):
        for obj in display_file.objects_list:
            self.objects[obj.name] = {"type": "", "indices": [], "color": obj.color}
            for coord in obj.coord:
                if coord not in self.edges:
                    self.edges.append(coord)
                self.objects[obj.name]["indices"].append(self.edges.index(coord) + 1)

            if obj.tipo == Type.POINT:
                self.objects[obj.name]["type"] = "p"
            elif obj.tipo == Type.WIREFRAME:
                self.objects[obj.name]["type"] = "f"
            else:
                self.objects[obj.name]["type"] = "l"

    def generateFileObj(self, name_file):
        mtl_filename = "cores.mtl"
        mtl_filepath = os.path.join("wavefront", mtl_filename)

        with open(mtl_filepath, "w") as mtl_file:
            mtl_file.write("")
        with open(name_file, "w") as obj_file:
            for i, edge in enumerate(self.edges):
                obj_file.write(f"v {edge[0]:.1f} {edge[1]:.1f} 0.0\n")

            obj_file.write(f"mtllib {mtl_filename}\n\n")

            print(self.objects.items())
            for name, data in self.objects.items():
                obj_file.write(f"o {name}\n")
                mtl_use = self._generateMTLFile(data["color"])
                obj_file.write(mtl_use)
                obj_file.write(f"{data['type']} {' '.join(map(str, data['indices']))}\n")

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
                return "usemtl Default\n"
        elif isinstance(color_data, QColor):
            return self.__process_qcolor_for_mtl(color_data)
        else:
            return "usemtl Default\n" 

    def __process_qcolor_for_mtl(self, qcolor: QColor) -> str:
        r_float, g_float, b_float, _ = qcolor.getRgbF()
        rgb_tuple_0_255 = (int(r_float * 255), int(g_float * 255), int(b_float * 255))
        color_name = f"Cor_{self.colors.setdefault(rgb_tuple_0_255, len(self.colors) + 1)}"
        mtl_filename = "cores.mtl"
        mtl_filepath = os.path.join("wavefront", mtl_filename)

        if rgb_tuple_0_255 in self.colors and self.colors[rgb_tuple_0_255] == len(self.colors):
            with open(mtl_filepath, "a") as mtl_file:
                mtl_file.write(f"newmtl {color_name}\n")
                mtl_file.write(f"Kd {rgb_tuple_0_255[0]} {rgb_tuple_0_255[1]} {rgb_tuple_0_255[2]}\n\n")

        return f"usemtl {color_name}\n"
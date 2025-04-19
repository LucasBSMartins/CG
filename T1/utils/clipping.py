from utils.setting import Type, ClippingAlgorithm

class Clipping:
    @staticmethod
    def clip(object_data, coordinates, viewing_window, clip_method):
        object_type = object_data.tipo
        if object_type == Type.POINT:
            return Clipping.clip_point(coordinates, viewing_window)
        elif object_type == Type.LINE:
            if clip_method == ClippingAlgorithm.COHEN:
                return Clipping.clip_line_cohen_sutherland(coordinates, viewing_window)
            else:
                return Clipping.clip_line_liang_barsky(coordinates, viewing_window)
        elif object_type == Type.WIREFRAME:
            return Clipping.clip_wireframe_sutherland_hodgeman(coordinates, viewing_window)

    @staticmethod
    def clip_point(point_coords, window):
        x, y = point_coords[0]
        if window.xmin_scn <= x <= window.xmax_scn and window.ymin_scn <= y <= window.ymax_scn:
            return True, point_coords
        else:
            return False, point_coords

    @staticmethod
    def clip_line_cohen_sutherland(line_coords, window):
        x1, y1 = line_coords[0]
        x2, y2 = line_coords[1]
        code1 = Clipping.get_cs_region_code(x1, y1, window)
        code2 = Clipping.get_cs_region_code(x2, y2, window)

        while True:
            if code1 == 0 and code2 == 0:
                return True, [[x1, y1], [x2, y2]]
            elif (code1 & code2) != 0:
                return False, line_coords
            else:
                outcode = code1 if code1 != 0 else code2

                if outcode & 0b0001:  # Left
                    m = (y2 - y1) / (x2 - x1) if (x2 - x1) != 0 else float('inf')
                    x = window.xmin_scn
                    y = m * (x - x1) + y1
                elif outcode & 0b0010:  # Right
                    m = (y2 - y1) / (x2 - x1) if (x2 - x1) != 0 else float('inf')
                    x = window.xmax_scn
                    y = m * (x - x1) + y1
                elif outcode & 0b0100:  # Bottom
                    m = (x2 - x1) / (y2 - y1) if (y2 - y1) != 0 else float('inf')
                    y = window.ymin_scn
                    x = x1 + m * (y - y1)
                elif outcode & 0b1000:  # Top
                    m = (x2 - x1) / (y2 - y1) if (y2 - y1) != 0 else float('inf')
                    y = window.ymax_scn
                    x = x1 + m * (y - y1)

                if outcode == code1:
                    x1, y1 = x, y
                    code1 = Clipping.get_cs_region_code(x1, y1, window)
                else:
                    x2, y2 = x, y
                    code2 = Clipping.get_cs_region_code(x2, y2, window)

    @staticmethod
    def get_cs_region_code(x, y, window):
        code = 0
        if x < window.xmin_scn:
            code |= 0b0001
        elif x > window.xmax_scn:
            code |= 0b0010
        if y < window.ymin_scn:
            code |= 0b0100
        elif y > window.ymax_scn:
            code |= 0b1000
        return code

    @staticmethod
    def clip_line_liang_barsky(line_coords, window):
        x1, y1 = line_coords[0]
        x2, y2 = line_coords[1]
        dx = x2 - x1
        dy = y2 - y1
        p = [-dx, dx, -dy, dy]
        q = [x1 - window.xmin_scn, window.xmax_scn - x1, y1 - window.ymin_scn, window.ymax_scn - y1]
        t_enter = 0
        t_exit = 1

        for i in range(4):
            if p[i] == 0:
                if q[i] < 0:
                    return False, line_coords
            else:
                t = q[i] / p[i]
                if p[i] < 0:
                    t_enter = max(t_enter, t)
                else:
                    t_exit = min(t_exit, t)

        if t_enter > t_exit:
            return False, line_coords

        new_x1 = x1 + t_enter * dx
        new_y1 = y1 + t_enter * dy
        new_x2 = x1 + t_exit * dx
        new_y2 = y1 + t_exit * dy
        return True, [[new_x1, new_y1], [new_x2, new_y2]]

    @staticmethod
    def clip_wireframe_sutherland_hodgeman(polygon_coords, window):
        clipping_edges = [
            (window.xmin_scn, window.ymin_scn, window.xmin_scn, window.ymax_scn),  # Left
            (window.xmin_scn, window.ymax_scn, window.xmax_scn, window.ymax_scn),  # Top
            (window.xmax_scn, window.ymax_scn, window.xmax_scn, window.ymin_scn),  # Right
            (window.xmax_scn, window.ymin_scn, window.xmin_scn, window.ymin_scn)   # Bottom
        ]

        clipped_polygon = list(polygon_coords)

        for edge in clipping_edges:
            new_polygon = []
            x1_clip, y1_clip, x2_clip, y2_clip = edge

            for i in range(len(clipped_polygon)):
                current_point = clipped_polygon[i]
                prev_point = clipped_polygon[i - 1] if i > 0 else clipped_polygon[-1]

                current_inside = Clipping.is_inside_sh(current_point, edge)
                prev_inside = Clipping.is_inside_sh(prev_point, edge)

                if current_inside:
                    if not prev_inside:
                        intersection = Clipping. get_intersection_sh(prev_point, current_point, edge)
                        new_polygon.append(intersection)
                    new_polygon.append(current_point)
                elif prev_inside:
                    intersection = Clipping.get_intersection_sh(prev_point, current_point, edge)
                    new_polygon.append(intersection)

            clipped_polygon = new_polygon

        if not clipped_polygon:
            return False, polygon_coords
        else:
            return True, clipped_polygon

    @staticmethod
    def is_inside_sh(point, edge):
        x_clip1, y_clip1, x_clip2, y_clip2 = edge
        return (x_clip2 - x_clip1) * (point[1] - y_clip1) - (y_clip2 - y_clip1) * (point[0] - x_clip1) > 0

    @staticmethod
    def get_intersection_sh(p1, p2, edge):
        x1, y1 = p1
        x2, y2 = p2
        x3, y3, x4, y4 = edge

        denominator = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
        if denominator == 0:
            return None  # Lines are parallel

        t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / denominator
        u = -((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)) / denominator

        if 0 <= t <= 1 and 0 <= u <= 1:
            intersection_x = x1 + t * (x2 - x1)
            intersection_y = y1 + t * (y2 - y1)
            return (intersection_x, intersection_y)
        return None
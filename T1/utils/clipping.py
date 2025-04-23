class Clipping:
    
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
    def clip_wireframe_sutherlandHodgeman(coords, window):
        clipping_window = [[window.xmin_scn, window.ymin_scn],
                       [window.xmin_scn, window.ymax_scn],
                       [window.xmax_scn, window.ymax_scn],
                       [window.xmax_scn, window.ymin_scn]]

        clipped_coords = coords
        for i in range(len(clipping_window)):
            previous_coords = clipped_coords
            clipped_coords = []
            window_edge1 = clipping_window[i]
            window_edge2 = clipping_window[(i+1)%len(clipping_window)]

            for j in range(len(previous_coords)):
                current_point = previous_coords[j]
                next_point = previous_coords[(j+1)%len(previous_coords)]

                current_inside = Clipping.is_inside_sh(current_point, window_edge1, window_edge2)
                next_inside = Clipping.is_inside_sh(next_point, window_edge1, window_edge2)
                
                if next_inside:
                    if not current_inside:
                        clipped_coords.append(Clipping.get_intersection_sh(current_point, next_point, window_edge1, window_edge2))
                    clipped_coords.append(next_point)
                elif current_inside:
                    clipped_coords.append(Clipping.get_intersection_sh(current_point, next_point, window_edge1, window_edge2))

        if len(clipped_coords) == 0:
            return (False, coords)
        else:
            return (True, clipped_coords)
   
    @staticmethod
    def is_inside_sh(point, edge1, edge2):
            return ((edge2[0]-edge1[0]) * (point[1]-edge1[1])) < ((edge2[1]-edge1[1]) * (point[0]-edge1[0]))

    @staticmethod
    def get_intersection_sh(point1, point2, edge1, edge2):
        numx = (edge1[0]*edge2[1] - edge1[1]*edge2[0])*(point1[0]-point2[0]) - (edge1[0]-edge2[0])*(point1[0]*point2[1]-point1[1]*point2[0])
        den = (edge1[0]-edge2[0])*(point1[1]-point2[1]) - (edge1[1]-edge2[1])*(point1[0]-point2[0])
        numy = (edge1[0]*edge2[1] - edge1[1]*edge2[0])*(point1[1]-point2[1]) - (edge1[1]-edge2[1])*(point1[0]*point2[1]-point1[1]*point2[0])
        return (numx/den, numy/den)
from objects.object import Object
from PySide6.QtGui import QPen, QColor
from utils.setting import Type, ClippingAlgorithm
from utils.clipping import Clipping
import numpy as np

class BSpline(Object):
    def __init__(self, name, control_points, color):
        """
        Initializes a BSplineCurve object.

        Args:
            name (str): The name of the BSpline curve.
            control_points (list): A list of control points (tuples of x, y coordinates).
            color (QColor): The color of the BSpline curve.
        """
        super().__init__(name, Type.B_SPLINE, control_points, color)

    def draw(self, window, painter, viewport, clipping_method, normalized_coords):
        """
        Draws the BSpline curve on the given painter.

        Args:
            window (Window): The current viewing window.
            painter (QPainter): The painter object to draw on.
            viewport (Viewport): The viewport transformation.
            clipping_method (ClippingMethod): The clipping method to use.
        """

        if len(normalized_coords) < 4:
            return  # Need at least 4 control points to draw a cubic B-Spline

        # Calculate the points along the B-Spline curve
        curve_points = self.__calculate_curve_points(normalized_coords)

        # Draw lines between the calculated points to approximate the curve
        pen = QPen(QColor(self.color), 3)
        painter.setPen(pen)

        for i in range(len(curve_points) - 1):
            point1 = curve_points[i]
            point2 = curve_points[i + 1]
            segment = [point1, point2]
            # Determine whether to draw the line segment (or part of it) after clipping
            if clipping_method == ClippingAlgorithm.COHEN:
                (draw, clipped_segment) = Clipping.clip_line_cohen_sutherland(segment, window)
            else:
                (draw, clipped_segment) = Clipping.clip_line_liang_barsky(segment, window)

            if draw:
                # Transform the clipped segment to viewport coordinates
                viewport_segment = viewport.calcularCoordsViewport(clipped_segment)

                # Draw the line segment
                painter.drawLine(
                    viewport_segment[0][0],
                    viewport_segment[0][1],
                    viewport_segment[1][0],
                    viewport_segment[1][1]
                )

    # Determine the points along the B-Spline curve to draw lines between
    def __calculate_curve_points(self, control_points):
        generated_points = []
        segment_precision = 50
        # Iterate over the control points in blocks of 4
        for i in range(3, len(control_points)):
            # Select the segment of 4 control points
            segment = control_points[i - 3:i + 1]

            # Calculate the initial conditions for forward differences for the segment
            x_initial, dx_initial, d2x_initial, d3x_initial, \
            y_initial, dy_initial, d2y_initial, d3y_initial = self.__get_initial_conditions(segment, (1 / segment_precision))

            generated_points.extend(self.__forward_difference_calculation(
                segment_precision,
                x_initial, dx_initial, d2x_initial, d3x_initial,
                y_initial, dy_initial, d2y_initial, d3y_initial
            ))
        return generated_points

    # Determine initial conditions for the forward difference algorithm
    def __get_initial_conditions(self, segment, step):
        # B-Spline basis matrix
        bspline_matrix = np.array([[-1 / 6, 3 / 6, -3 / 6, 1 / 6],
                                   [3 / 6, -1, 3 / 6, 0],
                                   [-3 / 6, 0, 3 / 6, 0],
                                   [1 / 6, 4 / 6, 1 / 6, 0]])

        # Geometry vectors for x and y coordinates of the segment
        x_geometry = [point[0] for point in segment]
        y_geometry = [point[1] for point in segment]

        # Coefficients for calculating initial conditions
        ax, bx, cx, dx = (np.dot(bspline_matrix, x_geometry)).tolist()
        ay, by, cy, dy = (np.dot(bspline_matrix, y_geometry)).tolist()

        step_squared = step**2
        step_cubed = step**3

        x_start = dx
        dx_start = ax * step_cubed + bx * step_squared + cx * step
        d2x_start = 6 * ax * step_cubed + 2 * bx * step_squared
        d3x_start = 6 * ax * step_cubed
        y_start = dy
        dy_start = ay * step_cubed + by * step_squared + cy * step
        d2y_start = 6 * ay * step_cubed + 2 * by * step_squared
        d3y_start = 6 * ay * step_cubed

        return x_start, dx_start, d2x_start, d3x_start, y_start, dy_start, d2y_start, d3y_start

    # Calculate points using the forward difference algorithm
    def __forward_difference_calculation(self, num_steps,
                                          x_current, dx, d2x, d3x,
                                          y_current, dy, d2y, d3y):
        points = [(x_current, y_current)]

        for _ in range(num_steps):
            x_current += dx
            dx += d2x
            d2x += d3x
            y_current += dy
            dy += d2y
            d2y += d3y
            points.append((x_current, y_current))
        return points
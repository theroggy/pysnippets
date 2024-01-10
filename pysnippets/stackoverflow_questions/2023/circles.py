import shapely
import shapely.plotting as sh_plot
from shapely.geometry import MultiLineString, MultiPoint, Polygon, Point
from shapely.ops import unary_union, polygonize
import matplotlib.pyplot as plt
import math
import numpy as np
import matplotlib as mpl

mpl.use("qt5agg")


def generate_hexagonal_grid(side_length, diameter):
    points = []
    radius = diameter / 2
    vertical_distance = np.sqrt(3) * radius
    x_max = side_length * np.cos(np.pi / 6)

    # Creating a hexagonal grid of points within the hexagon
    row = 0
    while (row * vertical_distance) < (2 * x_max):
        if row % 2 == 0:
            x_offset = diameter
        else:
            x_offset = radius

        x = -x_max + x_offset

        while x < x_max:
            y = -x_max + row * vertical_distance
            if np.abs(y) <= x_max:
                points.append((x, y))
            x += diameter

        row += 1

    return points


def draw_flat_topped_hexagon(apothem):
    s = 2 * apothem * math.tan(math.pi / 6)
    vertices = [
        (-apothem * math.tan(math.pi / 6), apothem),
        (apothem * math.tan(math.pi / 6), apothem),
        (2 * apothem * math.tan(math.pi / 6), 0),
        (apothem * math.tan(math.pi / 6), -apothem),
        (-apothem * math.tan(math.pi / 6), -apothem),
        (-2 * apothem * math.tan(math.pi / 6), 0),
    ]
    hexagon = Polygon(vertices)
    return hexagon


def fill_hexagon_with_circles(hexagon, points):
    # Initialize a plot
    fig, ax = plt.subplots()

    # Set the background color of the plot to black
    ax.set_facecolor("black")
    
    # List to store circle geometries
    circles = []
    occupied_area_center = []

    # Plot circles within the hexagon with black color
    i = 0
    for x, y in points:
        if i != int(len(points) / 2):
            point = Point(x, y)
            circle = point.buffer(0.5)  # Circle with diameter 1
            if circle.centroid not in occupied_area_center:
                if hexagon.contains(circle):
                    occupied_area_center.append(circle.centroid)
                    circles.append(circle)
                    x, y = circle.exterior.xy
                    ax.fill(x, y, alpha=1, fc="yellow", edgecolor="black")
        i += 1
    occupied_area = unary_union(circles)

    # Create a polygon that surrounds the circles by creating a convex hull
    surrounding_polygon = unary_union(circles).convex_hull

    # Calculate the surface area of a bead
    bead_area = math.pi * (0.5) ** 2

    # Calculate the target area
    max_packing_fraction = math.pi / (2 * math.sqrt(3))
    target_area = bead_area / max_packing_fraction
    vacant_space = surrounding_polygon.difference(occupied_area)

    # Subdivide the vacant space using delaunay triangles. The target area needs to
    # be divided by the number of triangles
    delaunays = shapely.get_parts(shapely.delaunay_triangles(MultiPoint(points)))
    vacant_areas = shapely.intersection(vacant_space, delaunays)
    # vacant_areas = list(polygonize(vacant_space.boundary))
    target_area /= 6

    # Plot points and delaunay edges to illustrate what is happening
    delaunay_edges = shapely.delaunay_triangles(MultiPoint(points), only_edges=True)
    sh_plot.plot_line(MultiLineString(delaunay_edges), color="green")
    sh_plot.plot_points(MultiPoint(points), color="orange")

    # Only retain sufficiently large areas
    valid_vacancies = [poly for poly in vacant_areas if poly.area > target_area]
    total_vacant_area = sum(poly.area for poly in valid_vacancies)
    for i, vacancy in enumerate(valid_vacancies):
        x, y = vacancy.exterior.xy
        ax.fill(x, y, alpha=0.5, fc="red", label=f"Vacancy {i + 1}")
    plt.grid(False)
    plt.show()


hex_diameter = 12
circle_diameter = 1.0

# Calculate the side length of the hexagon
side_length = hex_diameter * np.sqrt(3) / 2

# Generate a grid of points within the hexagon
points = generate_hexagonal_grid(side_length, circle_diameter)

# Create hexagon and fill it with circles
hexagon = draw_flat_topped_hexagon(hex_diameter)
fill_hexagon_with_circles(hexagon, points)

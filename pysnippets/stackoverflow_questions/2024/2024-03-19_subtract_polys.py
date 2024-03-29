from typing import TypedDict
from matplotlib import pyplot as plt
import shapely
from shapely.geometry import Polygon
from shapely.plotting import plot_polygon


class Coords(TypedDict):
    x: list[float]
    y: list[float]


def subtract_polygons(group_a: list[Coords], group_b: list[Coords]):
    # Convert polygons to Shapely Polygon objects
    polygons_a = [Polygon(zip(group["x"], group["y"])) for group in group_a]
    polygons_b = [Polygon(zip(group["x"], group["y"])) for group in group_b]

    # Create a "negative" polygon for the hole in group B
    negative_polygons_b = [Polygon(polygon.exterior) for polygon in polygons_b]

    # Subtract each polygon in polygons_b from each polygon in polygons_a
    result_polygons = []
    for polygon_a in polygons_a:
        result_polygon = polygon_a
        for negative_polygon_b in negative_polygons_b:
            result_polygon = result_polygon.difference(negative_polygon_b)

        result_polygons.append(result_polygon)

    return shapely.union_all(result_polygons)


group_a: list[Coords] = [
    {"x": [100, 200, 200, 100, 100], "y": [100, 100, 200, 200, 100]},
    {"x": [130, 230, 230, 130, 130], "y": [130, 130, 230, 230, 130]},
    {"x": [180, 280, 280, 180, 180], "y": [180, 180, 280, 280, 180]},
]
group_b: list[Coords] = [
    {"x": [150, 175, 175, 150, 150], "y": [150, 150, 175, 175, 150]},
    {"x": [150, 250, 250, 150, 150], "y": [220, 220, 320, 320, 220]},
]

result = subtract_polygons(group_a, group_b)

# Plot
polygons_a = [Polygon(zip(group["x"], group["y"])) for group in group_a]
polygons_b = [Polygon(zip(group["x"], group["y"])) for group in group_b]

for polygon_a in polygons_a:
    plot_polygon(polygon_a)
for polygon_b in polygons_b:
    plot_polygon(polygon_b, color="red")
plt.show()
plot_polygon(result)
plt.show()

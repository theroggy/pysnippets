from matplotlib import pyplot as plt
from shapely.geometry import Polygon
import shapely.plotting

poly = Polygon(
    [
        [263.84, 256.29],
        [268.6, 253.5],
        [269.57, 260.44],
        [277.2, 253.1],
        [278.94, 252.69],
        [278.56, 260.02],
        [278.76, 275.95],
        [288.99, 269.15],
        [263.84, 256.29],
    ]
)

centroid = poly.centroid
print(poly.wkt)
print(centroid.x, centroid.y)
print(f"poly.is_valid: {poly.is_valid}")

shapely.plotting.plot_polygon(poly)
plt.show()

poly_valid = shapely.make_valid(poly)
centroid_valid = poly_valid.centroid
print(poly_valid.wkt)
print(centroid_valid.x, centroid_valid.y)
print(f"poly_valid.is_valid: {poly_valid.is_valid}")

shapely.plotting.plot_polygon(poly_valid)
plt.show()

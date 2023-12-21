from matplotlib import pyplot as plt
import shapely.ops
import shapely.geometry
import shapely.plotting as plotter

p = shapely.geometry.Polygon(
    [
        (-250.0, 0.0),
        (-197.168784, 197.168784),
        (0.0, 250.0),
        (52.831216, 52.831216),
        (-52.831216, -52.831216),
        (-250.0, 0.0),
    ]
)
p = shapely.set_precision(p, grid_size=1e-6)
print(f"p.is_valid: {p.is_valid}")
print(f"p: {p}")
print(f"p.buffer(-0.00001): {p.buffer(-0.00001)}")
print(f"p.buffer(-0.0001)): {p.buffer(-0.0001)}")

p2 = shapely.Polygon(shapely.get_coordinates(p))
print(f"p2: {p2}")
print(f"p2.buffer(-0.00001): {p2.buffer(-0.00001)}")
p2 = p2.normalize()
print(f"p2 after normalize: {p2}")
print(f"p2.buffer(-0.00001): {p2.buffer(-0.00001)}")
p2 = shapely.set_precision(p2, grid_size=1e-6)
print(f"p2 after set_precision(p2, grid_size=1e-6): {p2}")
print(f"p2.get_precision: {shapely.get_precision(p2)}")
print(f"p2.buffer(-0.00001): {p2.buffer(-0.00001)}")

p2 = shapely.set_precision(p2, grid_size=0.0)
print(f"p2 after set_precision(p2, grid_size=0.0): {p2}")
print(f"p2.get_precision: {shapely.get_precision(p2)}")
print(f"p2.buffer(-0.00001): {p2.buffer(-0.00001)}")
p2_buffer = p2.buffer(-0.00001)
print(
    f"set_precision(p2_buffer, grid_size=1e-6): {shapely.set_precision(p2_buffer, grid_size=1e-6)}"
)
p2 = p2.normalize()
print(f"p2 after normalize: {p2}")
print(f"p2.buffer(-0.00001): {p2.buffer(-0.00001)}")

wkt = "POLYGON ((-197.168784 197.168784, 0 250, 52.831216 52.831216, -52.831216 -52.831216, -250 0, -197.168784 197.168784))"
p3 = shapely.from_wkt(wkt)
print(p3.buffer(-0.00001))

# plotter.plot_polygon(p)
plotter.plot_polygon(p.buffer(-0.0001))

plt.show()

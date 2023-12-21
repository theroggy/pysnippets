from matplotlib import pyplot as plt
import shapely.ops
import shapely.geometry
import shapely.plotting as plotter

print(f"shapely.__version__: {shapely.__version__}")
print(f"shapely.geos_version_string: {shapely.geos_version_string}")
print("----")

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

print("Original polygon: buffer(-0.00001) gives normal result, also after normalize")
print("----")
print(f"p: {p}")
print(f"p.is_valid: {p.is_valid}")
print(f"p.buffer(-0.00001): {p.buffer(-0.00001)}")
p = p.normalize()
print(f"p after normalize: {p}")
print(f"p.buffer(-0.00001): {p.buffer(-0.00001)}")
plotter.plot_polygon(p)
print("----")

print("After set_precision(p, grid_size=1e-6), the buffer result becomes EMPTY.")
print("----")
p2 = shapely.set_precision(p, grid_size=1e-6)
print(f"p2 after p2 = set_precision(p, grid_size=1e-6): {p2}")
print(f"p2.is_valid: {p2.is_valid}")
print(f"p2.buffer(-0.00001): {p2.buffer(-0.00001)}")
print(f"p2.buffer(-0.0001)): {p2.buffer(-0.0001)}")
print("----")

print("Verify that set_precision(p, grid_size=1e-6) didn't change any coordinates.")
print("----")
p2 = p2.normalize()
print(f"p after normalize: {p}")
print(f"p2 after normalize: {p2}")
print(f"p.wkt == p2.wkt: {p.wkt == p2.wkt}")
print(f"p.buffer(-0.00001): {p.buffer(-0.00001)}")
print(f"p2.buffer(-0.00001): {p2.buffer(-0.00001)}")
print("----")

print("If gridsize is reverted to 0.0 on p2, the buffer works fine again.")
print("----")
print(f"p2.get_precision: {shapely.get_precision(p2)}")
p2 = shapely.set_precision(p2, grid_size=0.0)
print(f"p2 after set_precision(p2, grid_size=0.0): {p2}")
print(f"p2.get_precision: {shapely.get_precision(p2)}")
print(f"p2.buffer(-0.00001): {p2.buffer(-0.00001)}")
print("----")

print("When set_precision(p2_buffer, grid_size=1e-6) is applied on the (correct) ")
print("result of p.buffer(-0.00001), it doesn't become empty.")
print("----")
p_buffer = p.buffer(-0.00001)
print(f"p_buffer = p.buffer(-0.00001): {p.buffer(-0.00001)}")
p_buffer2 = shapely.set_precision(p_buffer, grid_size=1e-6)
print(f"set_precision(p_buffer, grid_size=1e-6): {p_buffer2}")

plt.show()

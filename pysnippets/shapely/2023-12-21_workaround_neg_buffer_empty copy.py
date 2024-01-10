import shapely.ops
import shapely.geometry

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

p2 = shapely.set_precision(p, grid_size=1e-6)
print(f"p2.buffer(-0.00001): {p2.buffer(-0.00001)}")
p2 = shapely.set_precision(p2, grid_size=0.0)
print(f"p2.buffer(-0.00001), after set_precision(p2, grid_size=0.0): {p2.buffer(-0.00001)}")
p_buffer = p.buffer(-0.00001)
print(f"p_buffer: {p_buffer}")
p_buffer2 = shapely.set_precision(p_buffer, grid_size=1e-6)
print(f"p_buffer2 = shapely.set_precision(p_buffer, grid_size=1e-6): {p_buffer2}")

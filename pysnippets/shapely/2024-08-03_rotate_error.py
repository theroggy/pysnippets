from shapely import affinity
from shapely.geometry import Polygon

p0 = Polygon([(25, 50), (50, 50), (50, 75), (25, 0), (25, 50)])

p1 = affinity.rotate(p0, -15, origin=(0, 0))
print("T1", p1)

p0 = Polygon(
    [
        (25000000, 50000000),
        # (50000000, 50000000),
        (50000000, 75000000),
        (25000000, 0),
        (25000000, 50000000),
    ]
)

p1 = affinity.rotate(p0, -15, origin=(0, 0))
print("T2", p1)

p0 = Polygon(
    [
        (25000000, 50000000),
        (50000000, 50000000),
        (50000000, 75000000),
        (25000000, 0),
        (25000000, 50000000),
    ]
)

p1 = affinity.rotate(p0, -15, origin=(0, 0))
print("T3", p1)

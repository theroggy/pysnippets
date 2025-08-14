"""
ref: https://github.com/shapely/shapely/issues/1344
"""

from shapely.geometry import Polygon
import numpy as np

arr1 = np.array(
    [
        (84.74045967641753, 336.0128422648194),
        (657.1111793421711, 331.286320048389),
        (657.672168862722, 399.22083106930216),
        (85.30144919696846, 403.9473532857326),
    ]
)

arr2 = np.array(
    [
        (84.74045967641752, 336.0128422648194),
        (657.1111793421711, 331.286320048389),
        (657.6721688627221, 399.22083106930216),
        (85.30144919696846, 403.9473532857326),
    ]
)

p1_source = Polygon(arr1)
p2_source = Polygon(arr2)

p1_round32 = Polygon(arr1.round(32))
p2_round32 = Polygon(arr2.round(32))

p1_round18 = Polygon(arr1.round(18))
p2_round18 = Polygon(arr2.round(18))


print(p1_source == p2_source, p1_source.intersection(p2_source))
print(p1_round32 == p2_round32, p1_round32.intersection(p2_round32))
print(p1_round18 == p2_round18, p1_round18.intersection(p2_round18))
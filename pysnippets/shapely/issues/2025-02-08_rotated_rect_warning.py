from shapely.geometry import *
print(Polygon([Point(-100, -100), Point(-100, 100), Point(100, 100), Point(100, -100)]).minimum_rotated_rectangle)
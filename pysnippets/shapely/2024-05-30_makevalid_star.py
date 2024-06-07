import shapely
from shapely import Polygon, Point

xv = [0.5, 0.2, 1.0, 0, 0.8, 0.5]
yv = [1.0, 0.1, 0.7, 0.7, 0.1, 1]
xq = 0.5
yq = 0.6
polygon = Polygon(list(zip(xv, yv)))
poly_valid = shapely.make_valid(polygon, )
print(f"{polygon.contains(Point(xq, yq))}=")
print(f"{poly_valid.contains(Point(xq, yq))}=")

from shapely import Polygon, Point
import shapely

poly = Polygon([Point(0, 0), Point(1, 0), Point(1, 1), Point(0, 1)])
vertices = shapely.points(poly.exterior.coords)

for p in vertices:
    print(p)

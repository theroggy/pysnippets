import numpy as np
import shapely
from shapely import MultiPoint, Polygon
points = MultiPoint([(1,1), (2,2), (4,3), (2,4), (2,5), (6,5), (5,4), (7,1)])
myVoronoi = shapely.voronoi_polygons(points)

polygon_to_intersect = Polygon([(0,0), (2,8), (4,3.7), (10,4.5), (5,-4), (0,0)])

voronoi_polys = np.array(myVoronoi.geoms)
tree = shapely.STRtree(voronoi_polys)
intersecting_idx = tree.query(polygon_to_intersect, predicate="intersects")
intersections = shapely.intersection(voronoi_polys.take(intersecting_idx), polygon_to_intersect)
print(intersections)

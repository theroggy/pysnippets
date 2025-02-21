import numpy
import geopandas
import shapely
from shapely import ops, geometry
numpy.random.seed(8675309)
points = numpy.random.normal(size=(100,2))

# multipoint = shapely.unary_union([geometry.Point(c) for c in points])
multipoint = shapely.MultiPoint([geometry.Point(c) for c in points])

points_extracted = numpy.hstack([geom.xy for geom in multipoint.geoms]).T

assert points_extracted[0].tolist() == points[0].tolist() # No fail!

import numpy as np
import shapely
# from shapely.tests.common import all_types

# Make a GeometryCollection, then convert that to an array
# geom_collection = shapely.geometrycollections(all_types)
geom_collection = shapely.from_wkt('GEOMETRYCOLLECTION(GEOMETRYCOLLECTION(LINESTRING(0 0, 1 1)),LINESTRING(2 2, 3 3))')

geoms = np.array(geom_collection.geoms)

# Get a specific geometry type type
geoms[shapely.get_type_id(geoms) == shapely.GeometryType.LINESTRING]
# array([<LINESTRING (0 0, 1 0, 1 1)>], dtype=object)

# Get geometries with an inherent dimensionality
print(geoms[shapely.get_dimensions(geoms) == 0])
# array([<POINT (2 3)>, <MULTIPOINT (0 0, 1 2)>], dtype=object)

from shapely.geometry import Point, Polygon, MultiPoint
import geopandas as gpd
from geofileops.util._geoseries_util import harmonize_geometrytypes

poly = Polygon([(-1, -1), (-1, 2), (2, 2), (2, -1), (-1, -1)])
multipoint = MultiPoint([Point(0, 0), Point(1, 1)])
point = Point(0, 1)
point_ = Point(10, 10)
empty_point = Point()
none_point = Point()

gdf = gpd.GeoDataFrame(geometry=[multipoint, point, point_, empty_point, none_point])

# To generate a POINT EMPTY:
gdf["geometry"] = gdf["geometry"].apply(lambda x: x.intersection(poly))
gdf["geometry"].loc[4] = None  # special None case

print(f"{gdf=}")
# gdf=                    geometry
# 0  MULTIPOINT ((0 0), (1 1))
# 1                POINT (0 1)
# 2                POINT EMPTY
# 3                POINT EMPTY
# 4                       None

print(f"harmonize_geometrytypes\n{harmonize_geometrytypes(gdf.geometry)}")
# harmonize_geometrytypes
# 0    MULTIPOINT ((0 0), (1 1))
# 1           MULTIPOINT ((0 1))
# 2                         None
# 3                         None
# 4                         None
# Name: geometry, dtype: geometry

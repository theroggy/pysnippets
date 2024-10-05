import geopandas as gpd
from shapely import Polygon

# Input
poly1 = Polygon([(1, 1), (8, 1), (9, 9), (1, 8)])
poly2 = Polygon([(2, 1), (8, 1), (8, 8), (2, 8)])
poly3 = Polygon([(1, 2), (9, 2), (7, 9), (2, 8)])
gdf = gpd.GeoDataFrame(geometry=[poly1, poly2, poly3])

repr_point_gdf = gdf.representative_point()
print(type(repr_point_gdf))

repr_point_series = gdf.geometry.representative_point()
print(type(repr_point_series))

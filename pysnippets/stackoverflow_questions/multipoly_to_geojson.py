import geopandas as gpd
from shapely.geometry import MultiPolygon, Polygon
p1 = Polygon([(0, 0), (1, 0), (1, 1)])
p2 = Polygon([(5, 0), (6, 0), (6, 1)])
p3 = Polygon([(10, 0), (11, 0), (11, 1)])

d = {'number': [1, 2], 'geometry': [MultiPolygon([p1, p2]), MultiPolygon([p2, p3])]}
gdf = gpd.GeoDataFrame(d, crs="EPSG:31370")
print(gdf.to_json())

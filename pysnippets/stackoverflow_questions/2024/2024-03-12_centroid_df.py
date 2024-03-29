import geopandas as gpd
import shapely

p1 = shapely.Polygon([[0, 0], [0, 1], [1, 1], [0, 0]])
p2 = shapely.Polygon([[99, 99], [99, 100], [100, 100], [99, 99]])
df = gpd.GeoDataFrame(data={"desc": ["p1", "p2"]}, geometry=[p1, p2])

center = shapely.box(*df.total_bounds).centroid
print(center)
# POINT (50 50)

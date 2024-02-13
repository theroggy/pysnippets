import geopandas as gpd
import shapely

p1 = shapely.Polygon([[0, 20], [0, 30], [10, 30], [0, 20]])
p2 = shapely.Polygon([[0, 0], [0, 10], [10, 10], [0, 0]])
p3 = shapely.Polygon([[5, 0], [10, 1], [10, 0], [5, 0]])
gdf = gpd.GeoDataFrame(data={"desc": ["p1", "p2", "p3"]}, geometry=[p1, p2, p3])
path = "data.gpkg"
gdf.to_file(path)

print(gpd.read_file(path, mask=p3))

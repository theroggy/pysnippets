import shapely
import geopandas as gpd

line1 = shapely.LineString([(0, 0), (1, 0), (2, 0)])
line2 = shapely.LineString([(0, 1), (1, 1), (2, 1)])

gdf = gpd.GeoDataFrame(geometry=[line1, line2], crs=4326)
gdf["geom1"] = shapely.get_point(gdf.geometry, 0)
gdf["geom2"] = shapely.get_point(gdf.geometry, -1)

print(gdf[["geom1", "geom2"]])

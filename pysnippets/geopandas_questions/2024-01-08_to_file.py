import geopandas as gpd
from shapely import Polygon

polygon_a = Polygon(((0, 0), (10, 0), (10, 10), (0, 10), (0, 0)))
polygon_b = Polygon(((20, 20), (40, 20), (40, 40), (20, 40), (20, 20)))

# workaround 1: use pyogrio as I/O engine
a_series = gpd.GeoSeries([polygon_a])
b_series = gpd.GeoSeries([polygon_b])

a_series.to_file("./test_pyogrio.shp", engine="pyogrio")
b_series.to_file("./test_pyogrio.shp", engine="pyogrio", append=True)
b_series.to_file("./test_pyogrio.shp", engine="pyogrio", append=True)
print(gpd.read_file("./test_pyogrio.shp", engine="pyogrio", fid_as_index=True))

# workaround 2: use another format than .shp
a_series.to_file("./test.gpkg", engine="pyogrio")
b_series.to_file("./test.gpkg", engine="pyogrio", append=True)
b_series.to_file("./test.gpkg", engine="pyogrio", append=True)
print(gpd.read_file("./test.gpkg", engine="pyogrio", fid_as_index=True))

# workaround 3: add any attribute column
a_gdf = gpd.GeoDataFrame({"anycolumn": [1]}, geometry=[polygon_a])
b_gdf = gpd.GeoDataFrame({"anycolumn": [2]}, geometry=[polygon_b])

a_gdf.to_file("./test.shp", mode="w")
b_gdf.to_file("./test.shp", mode="a")
b_gdf.to_file("./test.shp", mode="a")
print(gpd.read_file("./test.shp", engine="pyogrio", fid_as_index=True))

import geopandas as gpd
import pyogrio
import shapely

gdf = gpd.GeoDataFrame(geometry=[shapely.box(0, 0, 10, 10)], crs="epsg:4326")

gpkg_path = "c:/temp/geoms.shz"
gdf.to_file(gpkg_path)

read_gdf = pyogrio.read_dataframe(gpkg_path)
print(read_gdf)

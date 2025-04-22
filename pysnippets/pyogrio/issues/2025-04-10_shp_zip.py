import geopandas as gpd
import geodatasets

gdf = gpd.read_file(geodatasets.get_path("nybb"))
gdf.to_file("out.path.shz")
read = gpd.read_file("out.path.shz") # this works fine

gdf.to_file("out2.shp.zip", engine='pyogrio', driver='ESRI Shapefile') # this fails with pyogrio, works with fiona
read = gpd.read_file("out2.shp.zip")

import tempfile
import pyogrio
import geopandas as gpd
import shapely


gdf = gpd.GeoDataFrame({"x": [0]}, geometry=[shapely.box(0,0,10,10)], crs=31370)

filename = f"{tempfile.gettempdir()}/test.gpkg.zip"
pyogrio.write_dataframe(gdf, filename)

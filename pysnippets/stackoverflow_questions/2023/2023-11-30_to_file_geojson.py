import geopandas as gpd
import shapely.geometry

s = gpd.GeoSeries([shapely.geometry.Point([10, 60])])
gdf = gpd.GeoDataFrame.from_dict(dict(geometry=s, col0=["val0"]))
gdf.to_file("2023-11-30_to_file_geojson.geojson", engine="pyogrio", id_generate=True)

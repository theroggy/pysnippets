import geopandas as pd

path = "C:/Temp/timezone/test.gpkg"
gdf = pd.read_file(path, engine="fiona")

print(gdf)

path = "C:/Temp/timezone/test.geojson"
gdf = pd.read_file(path, engine="fiona")

print(gdf)

path = "C:/Temp/timezone/test.gpkg"
gdf = pd.read_file(path, engine="pyogrio")

print(gdf)

path = "C:/Temp/timezone/test.geojson"
gdf = pd.read_file(path, engine="pyogrio")

print(gdf)

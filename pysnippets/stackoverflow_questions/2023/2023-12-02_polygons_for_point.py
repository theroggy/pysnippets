from datetime import datetime
import geopandas as gpd
from shapely import Point

start = datetime.now()
df = gpd.read_file("C:/Temp/prc2023/prc2023.shp", mask=Point(150000, 185000))
print(f"read .shp, found {len(df)} rows, took {datetime.now() - start}")

start = datetime.now()
df = gpd.read_file("C:/Temp/prc2023/prc2023.gpkg", mask=Point(150000, 185000))
print(f"read .gpkg, found {len(df)} rows, took {datetime.now() - start}")

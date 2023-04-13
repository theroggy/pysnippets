import datetime
from pathlib import Path

import geopandas as gpd


dir = Path("X:/PerPersoon/PIEROG/Taken/2023/2023-04-13_Testcase_slow_to_crs")
input_path = dir / "SD_County_Bike_Routes_2022_04.shp"

gdf = gpd.read_file(input_path)
assert isinstance(gdf, gpd.GeoDataFrame)

start_time = datetime.datetime.now()
gdf.to_crs(4326)
print(f"running gdf.to_crs(4326) took {datetime.datetime.now()-start_time}")
start_time = datetime.datetime.now()
gdf.to_crs(epsg=4326)
print(f"running gdf.to_crs(epsg=4326) took {datetime.datetime.now()-start_time}")
start_time = datetime.datetime.now()
gdf.geometry.to_crs(epsg=4326)
print(f"running gdf.geometry.to_crs(epsg=4326) took {datetime.datetime.now()-start_time}")

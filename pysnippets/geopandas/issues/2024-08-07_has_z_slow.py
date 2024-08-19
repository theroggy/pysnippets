import time
import geopandas as gpd


path = r"H:\Temp\tstdata\river_network.zip"
gdf = gpd.read_file(path)
print(f"{gdf=}")

start = time.perf_counter()
has_z = gdf.geometry.has_z
print(f"has_z took {time.perf_counter() - start} seconds")
print(f"{has_z=}")

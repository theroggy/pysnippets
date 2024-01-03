from datetime import datetime
import geopandas as gpd

path = "C:/Temp/prc2023/prc2023.gpkg"

"""
start = datetime.now()
gdf = gpd.read_file(path)
print(f"read_file took {datetime.now()-start} with fiona engine")
"""

"""
start = datetime.now()
gdf = gpd.read_file(path, engine="pyogrio")
print(f"read_file took {datetime.now()-start} with pyogrio engine")
"""

start = datetime.now()
gdf = gpd.read_file(path, engine="pyogrio", use_arrow=True)
print(f"read_file took {datetime.now()-start} with pyogrio engine and use_arrow=True")

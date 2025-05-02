from pathlib import Path

import geopandas as gpd

script_path = Path(__file__)
path = script_path.parent / "test_gdb_categories_nulls.gdb.zip"
gdf = gpd.read_file(path, engine="fiona")
print(gdf)
print(gdf.dtypes)

gdf = gpd.read_file(path)
print(gdf)
print(gdf.dtypes)

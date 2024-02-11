from pathlib import Path
import geopandas as gpd
import pandas as pd
import pyogrio
from shapely import Point

path = Path("test.gpkg")
path.unlink(missing_ok=True)
df = pd.DataFrame({"attr_table1_col": ["a1", "a2", "a3"]})
pyogrio.write_dataframe(df, path, layer="attr_table1")
gdf = gpd.GeoDataFrame({"point1_col": ["p1", "p2", "p3"]}, geometry=[Point(1, 2)] * 3)
pyogrio.write_dataframe(gdf, path, layer="point1")
gdf = gpd.GeoDataFrame({"point2_col": ["p1", "p2", "p3"]}, geometry=[Point(1, 2)] * 3)
pyogrio.write_dataframe(gdf, path, layer="point2")
df = pd.DataFrame({"attr_table2_col": ["a1", "a2", "a3"]})
pyogrio.write_dataframe(df, path, layer="attr_table2")
read_df = pyogrio.read_dataframe(path)
print(read_df)

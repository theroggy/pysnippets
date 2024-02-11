import pandas as pd
import geopandas as gpd
import shapely
from io import StringIO

# Toy example
csv_content = """fid,geom
1,"SRID=27700;POLYGON()"
2,"SRID=27700;POLYGON((10 10, 20 20, 30 10, 10 10))"
3,"SRID=27700;MULTIPOLYGON()"
"""

shlaa_df = pd.read_csv(StringIO(csv_content))

shlaa_df[["srid", "wkt"]] = shlaa_df["geom"].str.split(";", expand=True)
shlaa_df.loc[shlaa_df["wkt"] == "POLYGON()", "wkt"] = "POLYGON EMPTY"
shlaa_df.loc[shlaa_df["wkt"] == "MULTIPOLYGON()", "wkt"] = "MULTIPOLYGON EMPTY"
crs = shlaa_df.iloc[0]["srid"].split("=")[1]

shlaa_gdf = gpd.GeoDataFrame(geometry=shapely.from_wkt(shlaa_df["wkt"]), crs=crs)

print(shlaa_gdf)
print(shlaa_gdf.crs)

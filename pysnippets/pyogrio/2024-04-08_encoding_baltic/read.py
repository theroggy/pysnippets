from pathlib import Path
import geopandas as gpd

path = Path(__file__).resolve().parent / "R05_USER.DBF"
df = gpd.read_file(path, engine="fiona")
print(df.transpose())

# encoding="cp1257",
df = gpd.read_file(path, engine="pyogrio")
print(df.transpose())

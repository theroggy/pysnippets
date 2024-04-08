from pathlib import Path
import geopandas as gpd

path = Path(__file__).resolve().parent / "R05_USER.DBF"
df = gpd.read_file(path, encoding="cp1257")
print(df)

from pathlib import Path
import geopandas as gpd

path = Path(__file__).with_suffix(".geojson")
with open(path, 'r', encoding='latin') as f:
    data = f.read()
    gdf = gpd.read_file(data)

print(gdf.columns)

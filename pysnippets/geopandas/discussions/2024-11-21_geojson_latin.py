from pathlib import Path
import geopandas as gpd

path = Path(__file__).with_suffix(".geojson")
with open(path, 'r', encoding='latin') as file:
    gdf = gpd.read_file(file)

print(gdf.columns)

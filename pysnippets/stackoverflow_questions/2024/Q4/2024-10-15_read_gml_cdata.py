"""
https://stackoverflow.com/questions/79077483/geopandas-skipping-field-attribute-name-invalid-type-1-0
"""

from pathlib import Path
import geopandas as gpd

input_path = Path(__file__).resolve().with_suffix(".gml")
gdf = gpd.read_file(input_path)

print(gdf)

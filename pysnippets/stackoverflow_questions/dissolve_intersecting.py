import json
from pathlib import Path

import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd

script_dir = Path(__file__).resolve().parent
with open(script_dir / "dissolve_intersecting.geojson", "r") as f:
    data = json.load(f)

gdf = gpd.GeoDataFrame.from_features(data["features"])

# Calculate intersections within the layer
intersection_gdf = gdf.overlay(gdf, how="intersection", keep_geom_type=True)
intersection_gdf = intersection_gdf.loc[
    intersection_gdf.name_1 != intersection_gdf.name_2
]

# The features to dissolve are the intersecting one, excluding the self-intersections
to_dissolve_gdf = gdf.loc[
    gdf.name.isin(intersection_gdf.name_1) | gdf.name.isin(intersection_gdf.name_2)
]

# Other features should not be dissolved
no_dissolve_gdf = gdf.loc[~gdf.index.isin(to_dissolve_gdf.index)]

# Compile + plot the result
assert isinstance(to_dissolve_gdf, gpd.GeoDataFrame)
result_gdf = pd.concat([to_dissolve_gdf.dissolve(), no_dissolve_gdf])
result_gdf.plot(categorical=True, cmap="Set1", alpha=0.66)
plt.show()

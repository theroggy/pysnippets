import json
from pathlib import Path

import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd

url = "https://raw.githubusercontent.com/theroggy/pysnippets/07d778d3ac149b3ba2be22735d0a54bf3d52a6d7/pysnippets/stackoverflow_questions/2023-02-15_dissolve_intersecting.geojson"
gdf = gpd.read_file(url)

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

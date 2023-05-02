import geopandas as gpd
import pandas as pd

nybb_gdf = gpd.read_file(gpd.datasets.get_path("nybb"))

result_gdf = None
for row in nybb_gdf.itertuples():
    other_boro_gdf = nybb_gdf[nybb_gdf.index < row.Index]
    distances = other_boro_gdf.geometry.distance(row.geometry)
    distances_gdf = other_boro_gdf.copy()
    distances_gdf["distance"] = distances
    distances_gdf["from_index"] = row.Index
    distances_gdf["from_BoroName"] = row.BoroName

    if result_gdf is None:
        result_gdf = distances_gdf
    else:
        result_gdf = pd.concat([result_gdf, distances_gdf])

print(
    result_gdf[["BoroName", "from_BoroName", "distance"]].to_string(index=False)
)

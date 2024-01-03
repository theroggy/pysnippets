import geopandas as gpd
import pandas as pd

# path = "states.shp"
path = gpd.datasets.get_path("nybb")
gdf = gpd.read_file(path)

# Convert to "USA Contiguous Equidistant Conic" to get OK distances for USA
# gdf = gdf.to_crs("ESRI:102005")

result_gdf = None
for row in gdf.itertuples():
    other_gdf = gdf[gdf.index < row.Index]
    distances = other_gdf.geometry.distance(row.geometry)
    distances_gdf = other_gdf.copy()
    distances_gdf["distance"] = distances
    for name, value in row._asdict().items():
        distances_gdf[f"to_{name}"] = value

    if result_gdf is None:
        result_gdf = distances_gdf
    else:
        result_gdf = pd.concat([result_gdf, distances_gdf])

print(result_gdf[["BoroName", "to_BoroName", "distance"]].to_string(index=False))

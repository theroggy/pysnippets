import geopandas as gpd
import pandas as pd

gdf = gpd.read_file(gpd.datasets.get_path("nybb"))

result_gdf = None
for row in gdf.itertuples():
    row_gdf = gpd.GeoDataFrame([row], crs=gdf.crs)
    other_gdf = gdf[gdf.index != row.Index]
    nearest_other_gdf = row_gdf.sjoin_nearest(
        other_gdf, distance_col="distance"
    )
    if result_gdf is None:
        result_gdf = nearest_other_gdf
    else:
        result_gdf = pd.concat([result_gdf, nearest_other_gdf])

print(
    result_gdf[["BoroName_left", "BoroName_right", "distance"]].to_string(index=False)
)

import geopandas as gpd
import pandas as pd

countries_gdf = gpd.read_file(gpd.datasets.get_path("nybb"))

result_gdf = None
for row in countries_gdf.itertuples():
    cur_country_gdf = gpd.GeoDataFrame([row], crs=countries_gdf.crs)
    other_countries_gdf = countries_gdf[countries_gdf.index != row.Index]
    nearest_other_gdf = cur_country_gdf.sjoin_nearest(
        other_countries_gdf, distance_col="distance"
    )
    if result_gdf is None:
        result_gdf = nearest_other_gdf
    else:
        result_gdf = pd.concat([result_gdf, nearest_other_gdf])

print(
    result_gdf[["BoroName_left", "BoroName_right", "distance"]].to_string(index=False)
)

import geopandas as gpd

gdf = gpd.read_file(gpd.datasets.get_path("nybb"))
for row in gdf.itertuples():
    print(
        f"row with index {row.Index} has BoroName <{row.BoroName}> and Shape_Area is "
        f"<{gdf['Shape_Area'][row.Index]}>"
    )

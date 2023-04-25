import geopandas as gpd
from shapely import Point

file_gdf = gpd.GeoDataFrame(geometry=[Point(10, 10), Point(10, 0), Point(-15, 0)])
search_point = Point(1, 1)

search_point_gdf = gpd.GeoDataFrame(geometry=[search_point], crs=file_gdf.crs)
nearest_in_file_gdf = search_point_gdf.sjoin_nearest(
    file_gdf[["geometry"]], distance_col="distance", rsuffix="nearest"
).set_index("index_nearest")
nearest_in_file_gdf = nearest_in_file_gdf.join(file_gdf, rsuffix="_nearest")
print(nearest_in_file_gdf)

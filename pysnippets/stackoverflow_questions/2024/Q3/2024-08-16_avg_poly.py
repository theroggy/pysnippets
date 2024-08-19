import geopandas as gpd
from matplotlib import pyplot as plt
from shapely.geometry import Polygon
from shapely.plotting import plot_polygon

# Input
poly1 = Polygon([(1, 1), (8, 1), (9, 9), (1, 8)])
poly2 = Polygon([(2, 1), (8, 1), (8, 8), (2, 8)])
poly3 = Polygon([(1, 2), (9, 2), (7, 9), (2, 8)])
gdf = gpd.GeoDataFrame(geometry=[poly1, poly2, poly3])
gdf["id"] = gdf.index

# Do a self-overlay to split up the polygons in smaller parts
union_gdf = gdf.overlay(gdf, how="union", keep_geom_type=True)
# Remove the result of self-intersection of the same polygons
union_gdf = union_gdf.loc[union_gdf["id_1"] != union_gdf["id_2"]]
# Dissolve again
union_gdf.geometry = union_gdf.geometry.normalize()
union_diss_gdf = gpd.GeoDataFrame(
    union_gdf.groupby(["geometry"])[["id_1"]]
    .count()
    .reset_index()
    .rename(columns={"id_1": "count"})
)

# Only retain areas where count is at least 2
average_gdf = union_diss_gdf[union_diss_gdf["count"] >= 2]
average_gdf = average_gdf.dissolve()

_, ax = plt.subplots()
plot_polygon(poly1, ax=ax, color="green", facecolor="none")
plot_polygon(poly2, ax=ax, color="blue", facecolor="none")
plot_polygon(poly3, ax=ax, color="yellow", facecolor="none")
plot_polygon(average_gdf.geometry[0], ax=ax, color="red", facecolor="none", hatch="/")
plt.show()

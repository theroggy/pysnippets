from matplotlib import pyplot as plt
import numpy as np
import shapely
import geopandas as gpd


def define_spot_grid(gdf_base_grid, size_base, size_swath):
    # First create gdf with all possible bigger spots, covering the bounds of
    # gdf_base_grid.
    # Remark: because we want to find all possible bigger spots with the number of small
    # spots asked, the bigger spots will overlap. 
    bounds = gdf_base_grid.total_bounds
    bigger_spots = []
    for xmin in np.arange(bounds[0], bounds[2], size_base):
        for ymin in np.arange(bounds[1], bounds[3], size_base):
            bigger_spots.append(
                shapely.geometry.box(xmin, ymin, xmin + size_swath, ymin + size_swath)
            )
    bigger_spots_gdf = gpd.GeoDataFrame(geometry=bigger_spots, crs=gdf_base_grid.crs)

    # Check for each bigger spot how many small spots intersect with it. Join with
    # centroids of base grid to avoid spots that only touch being counted.
    base_grid_centroid_gdf = gpd.GeoDataFrame(
        geometry=gdf_base_grid.centroid, crs=gdf_base_grid.crs
    )
    sjoin_gdf = bigger_spots_gdf.sjoin(
        base_grid_centroid_gdf, how="inner", predicate="intersects"
    )
    number_small_in_bigger_df = sjoin_gdf[["index_right"]].groupby(level=0).count()

    # Only keep bigger spots with the minimum needed number small ones in them.
    minimum = (size_swath/size_base) ** 2
    indices_to_keep = number_small_in_bigger_df[
        number_small_in_bigger_df.index_right >= minimum
    ].index.tolist()

    return bigger_spots_gdf.loc[indices_to_keep]

# Init parameters
size_base = 1

# Create base grid
a0 = shapely.geometry.Point([0, 0]).buffer(size_base / 2, cap_style="square")
a1 = shapely.affinity.translate(a0, xoff=1)
a2 = shapely.affinity.translate(a0, xoff=2)
a3 = shapely.affinity.translate(a0, xoff=3)
a4 = shapely.affinity.translate(a0, xoff=4)

b0 = shapely.affinity.translate(a0, yoff=1)
b1 = shapely.affinity.translate(b0, xoff=1)
b2 = shapely.affinity.translate(b0, xoff=2)
b3 = shapely.affinity.translate(b0, xoff=3)
b4 = shapely.affinity.translate(b0, xoff=4)

c0 = shapely.affinity.translate(b0, yoff=1)
c1 = shapely.affinity.translate(c0, xoff=1)
c2 = shapely.affinity.translate(c0, xoff=2)
c3 = shapely.affinity.translate(c0, xoff=3)

liste_geo = [a0, a1, a2, a3, a4, b0, b1, b2, b3, b4, c0, c1, c2, c3]
column = [1, 2, 3, 4, 5, 1, 2, 3, 4, 5, 1, 2, 3, 4]
row = [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 2, 2, 2, 2]

gdf_base_grid = gpd.GeoDataFrame(
    {"column": column, "row": row, "geometry": liste_geo},
    crs="epsg:4326",
    index=range(len(liste_geo)),
)

# Calculate for swath size * 2
size_swath = size_base * 2
bigger_gdf = define_spot_grid(gdf_base_grid, size_base, size_swath)
f, ax = plt.subplots()
gdf_base_grid.plot(ax=ax, facecolor="none")
bigger_gdf.plot(ax=ax, facecolor="none", edgecolor="red", linewidth=2)
plt.show()

# Calculate for swath size * 3
size_swath = size_base * 3
bigger_gdf = define_spot_grid(gdf_base_grid, size_base, size_swath)
f, ax = plt.subplots()
gdf_base_grid.plot(ax=ax, facecolor="none")
bigger_gdf.plot(ax=ax, facecolor="none", edgecolor="red", linewidth=2)
plt.show()

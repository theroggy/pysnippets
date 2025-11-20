import geopandas as gpd
import pygeoops
import shapely
import matplotlib.pyplot as plt

wkt = "POLYGON ((3 0, 9 0, 7 2, 7 10, 12 10, 12 12, 0 12, 0 10, 5 10, 5 2, 3 0))"
poly = shapely.from_wkt(wkt)
poly_gdf = gpd.GeoDataFrame([{"name": "T-shape", "geometry": poly}], crs="epsg:31370")

figure, (ax1, ax2, ax3) = plt.subplots(nrows=1, ncols=3, figsize=(6, 3), dpi=90)

# First subplot: no cleanup
ax1.set_title("min_branch_length=0")
centerline1_gdf = poly_gdf.copy()
centerline1_gdf.geometry = pygeoops.centerline(centerline1_gdf.geometry, min_branch_length=0)

poly_gdf.plot(ax=ax1, color="lightgray", edgecolor="black")
centerline1_gdf.plot(ax=ax1, color="red", linewidth=2)

# Second subplot: default options
ax2.set_title("default")
centerline2_gdf = poly_gdf.copy()
centerline2_gdf.geometry = pygeoops.centerline(centerline2_gdf.geometry)

poly_gdf.plot(ax=ax2, color="lightgray", edgecolor="black")
centerline2_gdf.plot(ax=ax2, color="red", linewidth=2)

# Third subplot: min_branch_length=-2
ax3.set_title("min_branch_length=-2")
centerline3_gdf = poly_gdf.copy()
centerline3_gdf.geometry = pygeoops.centerline(centerline3_gdf.geometry, min_branch_length=-2)

poly_gdf.plot(ax=ax3, color="lightgray", edgecolor="black")
centerline3_gdf.plot(ax=ax3, color="red", linewidth=2)

plt.show()

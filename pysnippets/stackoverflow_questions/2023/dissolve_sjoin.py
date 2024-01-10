import geopandas as gpd
from matplotlib import pyplot as plt
import shapely

# Prepare test data
row, col = (0, 0)
nb = 4
rects = []
colors = []
row_nbs = []
size = 10
while row <= nb:
    color = "orange"
    if (row % 2) == 0:
        color = "grey"
    while col <= row and col <= nb:
        rect = (col*size, row*size, col*size + size, row*size + size)
        rects.append(rect)
        colors.append(color)
        row_nbs.append(row)
        col += 1
    col = 0
    row += 1

geoms = [shapely.box(*rect) for rect in rects]
gdf = gpd.GeoDataFrame({"color": colors, "row_nb": row_nbs, "geometry": geoms}, crs=31370)  # type: ignore
print(f"Test dataset:\n{gdf}")

# Dissolve + explode the test dataset
dissolve_gdf = gdf.dissolve(by=["color", "row_nb"]).explode().reset_index()  # type: ignore
print(f"\ndissolve_gdf:\n{dissolve_gdf}")

# sjoin both
joined_gdf = gdf.sjoin(dissolve_gdf, predicate="within")
print(f"\nresult_gdf:\n{joined_gdf}")

counts_df = joined_gdf.groupby(["row_nb_right", "color_right"]).size()
print(f"\ncounts_df:\n{counts_df}")

gdf.plot(color=gdf["color"], edgecolor="black")
plt.show()

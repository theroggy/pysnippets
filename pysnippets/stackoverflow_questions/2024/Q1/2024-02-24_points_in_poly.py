import geopandas as gpd
from matplotlib import pyplot as plt
from shapely import box, Point

# Create some test data
polys = gpd.GeoDataFrame(
    geometry=[
        box(xmin=xmin, ymin=ymin, xmax=xmin + 10, ymax=ymin + 10)
        for xmin in range(0, 100, 10)
        for ymin in range(0, 100, 10)
    ],
    crs=31370,
)
points = gpd.GeoDataFrame(
    geometry=[Point(50, 50), Point(55, 55), Point(200, 50)], crs=31370
)

# Find all intersections between points and polygons, using a spatial index for speed.
# The first result of `query` contains all integer indexes of all points where at least
# one intersection was found.
points_in_poly_idx = polys.sindex.query(points.geometry, predicate="intersects")[0]
# Exclude all points where an intersection was found.
points_outside_polys = points.loc[~points.index.isin(points_in_poly_idx)]

print(len(points_outside_polys))
# One point outside of the polygons

fig, ax = plt.subplots()
polys.plot(ax=ax, edgecolor="blue", facecolor="none")
points.plot(ax=ax, color="red")
points_outside_polys.plot(ax=ax, color="green")
plt.show()

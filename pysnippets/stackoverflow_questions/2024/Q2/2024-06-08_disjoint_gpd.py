"""
https://gis.stackexchange.com/questions/483220/clip-data-in-geopandas-to-keep-everything-not-in-polygons
"""

import geopandas as gpd

from shapely import box, Point
import matplotlib.pyplot as plt

# Some test data
polys = gpd.GeoDataFrame(
    data={
        "poly_name": ["poly_left", "poly_right"],
        "geometry": [box(0, 0, 2, 2), box(4, 0, 6, 2)],
    }
)
points = gpd.GeoDataFrame(
    {
        "point_name": ["point1", "point2", "point3", "point4"],
        "geometry": [Point(3, 0), Point(1, 1), Point(7, 1), Point(5, 1)],
    },
)

# Join the points that intersect with the polygons.
# This uses an rtree under the hood, so is fast.
points_intersects = points.sjoin(polys, predicate="intersects")

# Now only retain the points that don't intersect.
points_disjoint = points.loc[~points.index.isin(points_intersects.index)]

# Print result
print(points_disjoint)

# Plot input data and result
fig, ax = plt.subplots()
polys.plot(ax=ax, edgecolor="red", facecolor="none")
points.plot(
    ax=ax,
    color="blue",
    facecolor="none",
)
points_disjoint.plot(ax=ax, edgecolor="green", facecolor="none")
plt.show()

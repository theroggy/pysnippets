import geopandas as gpd
from matplotlib import pyplot as plt
import shapely
from shapely.geometry import Point

# Prepare test data
circles = gpd.GeoDataFrame(
    {
        "circle_name": ["circle1", "circle2", "circle3"],
        "geometry": [Point(20, 20), Point(30, 20), Point(25, 12)],
    }
)
circles.geometry = circles.buffer(8)

# Create a "flat union" of the input polygons
union_flat = gpd.GeoDataFrame(
    geometry=shapely.get_parts(
        shapely.polygonize(
            shapely.get_parts(shapely.union_all(circles.geometry.boundary))
        )
    ),
    crs=circles.crs,
)
print(f"{len(union_flat)=}")

# Perform intersection
union = circles.overlay(union_flat, how="intersection", keep_geom_type=True)
print(f"{len(union)=}")

# Plot result
ax = circles.plot(facecolor="none")
union.plot(ax=ax, facecolor="none")
plt.show()

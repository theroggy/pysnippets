from matplotlib import pyplot as plt
import pygeoops
from pygeoops._centerline import _remove_short_branches
import shapely
import shapely.plotting as plotter

# Sample data.
wkt = "POLYGON((0 0,0 8,-4 8,-4 10,0 10,0 14,2 14,2 9,4 9,4 8,2 8,2 2,10 2,10 0,2 0,2 -5,0 -5,0 0))"
river = shapely.from_wkt(wkt)

# Calculate centerline.
river_center = pygeoops.centerline(river)
# Determine main river. Not the ideal algorith, but it's only a POC, and it shows the idea.
main_river_center = _remove_short_branches(
    river_center, min_branch_length=5, remove_one_by_one=True
)

# Split river to delaunay triangles + clip to the river polygon.
river_triangles = shapely.delaunay_triangles(river)
river_triangles_clip = pygeoops.collection_extract(
    shapely.intersection(shapely.get_parts(river_triangles), river),
    primitivetype=pygeoops.PrimitiveType.POLYGON,
)
river_triangles_clip = [poly for poly in river_triangles_clip if poly is not None]

# Form the tributaries from the triangles not intersecting the main river centerline.
river_triangles_clip = [
    poly
    for poly in river_triangles_clip
    if not shapely.intersects(poly, main_river_center)
]
tributaries = shapely.get_parts(shapely.union_all(river_triangles_clip))

# Remove the tributaries from the river.
main_river = pygeoops.difference_all(river, tributaries, keep_geom_type=True)

# Plot
plotter.plot_polygon(river)
plotter.plot_line(main_river_center)
plotter.plot_polygon(main_river, color="green")

plt.show()

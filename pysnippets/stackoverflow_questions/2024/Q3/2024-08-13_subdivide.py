import pygeoops
from shapely import box


poly = box(0, 0, 10, 10)

poly_sub = pygeoops.subdivide(poly, num_coords_max=3)

print(f"{poly=}")
print(f"{poly_sub=}")
# poly=<POLYGON ((10 0, 10 10, 0 10, 0 0, 10 0))>
# poly_sub=array([<POLYGON ((5 10, 5 0, 0 0, 0 10, 5 10))>,
#        <POLYGON ((10 0, 5 0, 5 10, 10 10, 10 0))>], dtype=object)

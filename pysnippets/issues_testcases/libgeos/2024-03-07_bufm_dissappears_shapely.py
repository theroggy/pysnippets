"""
Reported here: https://github.com/shapely/shapely/issues/2009
And upstreamed here: https://github.com/libgeos/geos/issues/984
"""

from matplotlib import pyplot as plt
import shapely
import shapely.plotting

wkt = "POLYGON ((-8486160.859752608 4407005.311912118, -8486322.012133999 4419552.266313265, -8498821.965759974 4419382.682467878, -8498646.158633558 4406836.479565462, -8486160.859752608 4407005.311912118))"

poly = shapely.from_wkt(wkt)
poly_bufm = shapely.buffer(poly, distance=1e-11)

print(f"{poly.is_valid=}")
print(f"{poly_bufm.is_valid=}")
print(f"{poly_bufm=}")

shapely.plotting.plot_polygon(poly)
shapely.plotting.plot_polygon(poly_bufm, color="red")
plt.show()

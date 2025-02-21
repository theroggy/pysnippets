import matplotlib.pyplot as plt
from shapely import wkt
from shapely import plotting

poly = wkt.loads(
    "POLYGON ((2653.9 425.9100000000003, 2653.8999999999996 1067.39, 1331.61 1067.3900000000003, 1331.61 1223.5586000000003, 2653.9 1223.5586000000003, 2653.9 425.9100000000003))"
)
print(f"{poly.is_valid=}") # prints True
rp = poly.representative_point()
print(f"{rp=}") # prints False
print(f"{poly.intersects(rp)=}") # prints False

plotting.plot_polygon(poly)
plotting.plot_points(rp, color="red")
plt.show()

"""
Added to geos issue: https://github.com/libgeos/geos/issues/984
"""

from matplotlib import pyplot as plt
import shapely
import shapely.plotting

wkt = "POLYGON ((189830.82937655927 236280.33651798425, 189826.6517640246 236284.73029061654, 189890.06437987628 236413.14271446358, 189896.17545283484 236412.43408390653, 189917.96066382117 236318.46340062976, 189917.6788285035 236317.90492723353, 189830.82937655927 236280.33651798425))"
poly = shapely.from_wkt(wkt)
poly_bufm5 = shapely.buffer(poly, distance=-5)

print(f"poly.is_valid: {poly.is_valid}")
print(f"poly_bufp5m5.is_valid: {poly_bufm5.is_valid}")

shapely.plotting.plot_polygon(poly)
shapely.plotting.plot_polygon(poly_bufm5, color="red")
plt.show()

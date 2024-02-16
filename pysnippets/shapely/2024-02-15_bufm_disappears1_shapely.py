"""
Added to geos issue: https://github.com/libgeos/geos/issues/984
"""

from matplotlib import pyplot as plt
import shapely
import shapely.plotting

wkt = "Polygon ((182719.04521570954238996 224897.14115349075291306, 182807.02887436276068911 224880.64421749324537814, 182808.47314301913138479 224877.25002362736267969, 182718.38701137207681313 224740.00115247094072402, 182711.82697281913715415 224742.08599378637154587, 182717.1393717635946814 224895.61432328051887453, 182719.04521570954238996 224897.14115349075291306))"

poly = shapely.from_wkt(wkt)
poly_bufm = shapely.buffer(
    poly, distance=-5, #join_style="mitre", mitre_limit=2.0,
)

print(f"poly.is_valid: {poly.is_valid}")
print(f"poly_bufm.is_valid: {poly_bufm.is_valid}")

shapely.plotting.plot_polygon(poly)
shapely.plotting.plot_polygon(poly_bufm, color="red")
plt.show()

import pygeoops
import shapely
import shapely.plotting as plot
import matplotlib.pyplot as plt

wkt = """MultiPolygon (((64440.00000007346534403 218000.00000000279396772, 64438.00000007345079212 218000.00000000279396772, 64438.00000007345079212 218000.00000000311410986, 64440.00000007346534403 218000.00000000311410986, 64440.00000007346534403 218000.00000000279396772)))"""
poly = shapely.from_wkt(wkt)
print(f"{poly.is_valid=}")
print(f"{poly.area=}")
plot.plot_polygon(poly)
plt.show()

centerline = pygeoops.centerline(poly, densify_distance=0)
print(f"{centerline=}")

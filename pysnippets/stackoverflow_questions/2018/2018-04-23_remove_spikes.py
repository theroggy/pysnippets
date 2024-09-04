from matplotlib import pyplot as plt
import shapely
from shapely.plotting import plot_polygon

wkt = "POLYGON ((6.980710220282101 51.243221513354044, 6.980706911073409 51.24322119551712, 6.9806699432069745 51.24337283218559, 6.980864165775662 51.24339148636556, 6.980901140490866 51.24323981899073, 6.980795641198141 51.24322968631755, 6.980776365429034 51.243308752807856, 6.980690951372498 51.243300549145346, 6.980710220282101 51.243221513354044))"
poly = shapely.from_wkt(wkt)

from shapely.geometry import shape

test = {"type": "FeatureCollection", "features": [{"id": "0", "type": "Feature", "properties": {}, "geometry": {"type": "Polygon", "coordinates": [[[6.980710220282101, 51.243221513354044], [6.980706911073409, 51.24322119551712], [6.9806699432069745, 51.24337283218559], [6.980864165775662, 51.24339148636556], [6.980901140490866, 51.24323981899073], [6.980795641198141, 51.24322968631755], [6.980776365429034, 51.243308752807856], [6.980690951372498, 51.243300549145346], [6.980710220282101, 51.243221513354044]]]}}]}
poly = shape(test["features"][0]["geometry"])

d = 0.00001  # distance
cf = 1.3  # cofactor
p_buf_simpl = poly.buffer(-d).buffer(d * cf).intersection(poly).simplify(d)

fig, ax = plt.subplots()
plot_polygon(poly, ax=ax, color="red")
plot_polygon(p_buf_simpl, ax=ax, color="blue")
ax.set_aspect("equal", "box")
plt.show()

p_buf_mitre = poly.buffer(-d, join_style="mitre").buffer(d, join_style="mitre")

fig, ax = plt.subplots()
plot_polygon(poly, ax=ax, color="red")
plot_polygon(p_buf_mitre, ax=ax, color="blue")
ax.set_aspect("equal", "box")
plt.show()

p_prec = shapely.set_precision(poly, grid_size=d/2)

fig, ax = plt.subplots()
plot_polygon(poly, ax=ax, color="red")
plot_polygon(p_prec, ax=ax, color="blue")
ax.set_aspect("equal", "box")
plt.show()

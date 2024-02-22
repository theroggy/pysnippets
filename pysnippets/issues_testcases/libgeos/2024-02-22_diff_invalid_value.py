from matplotlib import pyplot as plt
import shapely
import shapely.plotting

wkt1 = "POLYGON ((131914.3 165394.91, 131914.75 165401.13, 131915.4 165405.16, 131916.98999999982 165412.2699999993, 131917.01000000004 165412.35000000012, 131918.6075124378 165417.54999999996, 131934.1788562094 165417.54999999996, 131939.09337653648 165416.6004541625, 131939.3088653061 165417.54999999996, 131951.57623509367 165417.54999999996, 131950.86761972334 165414.32552540785, 131970.79499999998 165410.47531018153, 131970.79499999998 165383.46209010988, 131950.52097650486 165387.570364761, 131948.83624341668 165390.12270711953, 131946.2664836365 165388.4278781114, 131914.3 165394.91))"  # noqa: E501
wkt2 = "POLYGON ((131914.3 165394.91, 131914.75 165401.13, 131915.4 165405.16, 131916.99 165412.27, 131917.01 165412.35, 131918.6075124378 165417.54999999996, 131934.17885620942 165417.54999999996, 131970.79499999998 165410.47531018153, 131970.79499999998 165383.46209010988, 131952.25 165387.22, 131952.31 165387.51, 131952.35 165387.71, 131944.64 165389.31, 131944.53 165388.78, 131914.3 165394.91))"  # noqa: E501
poly1 = shapely.from_wkt(wkt1)
poly2 = shapely.from_wkt(wkt2)

"""
xmin = poly1.bounds[0] + 950
ymin = poly1.bounds[1] + 750
rect = (xmin, ymin, xmin + 80, ymin + 125)
poly1 = shapely.clip_by_rect(poly1, *rect)
poly2 = shapely.clip_by_rect(poly2, *rect)

print(f"{shapely.get_num_coordinates(poly1)=}")
print(f"{shapely.get_num_coordinates(poly2)=}")
"""

print(f"{poly1.is_valid=}")
print(f"{poly2.is_valid=}")

diff = shapely.difference(poly1, poly2)

print(f"{shapely.get_num_coordinates(diff)=}")

shapely.plotting.plot_polygon(diff, facecolor="green", edgecolor="green", add_points=False, alpha=0.3)
shapely.plotting.plot_polygon(poly1, facecolor="none", edgecolor="blue", add_points=False, hatch="\\")
shapely.plotting.plot_polygon(poly2, facecolor="none", edgecolor="red", add_points=False, hatch="/")
plt.show()

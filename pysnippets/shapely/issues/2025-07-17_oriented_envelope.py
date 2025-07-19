import matplotlib.pyplot as plt
import shapely
from shapely.geometry import LineString
from shapely.set_operations import union_all
from shapely import plotting

line1 = LineString([(1418998483.493762, 4185936458.970139), (1419000750.412936, 4185935752.893123)])
line2 = LineString([(1418991903.483397, 4185938508.444688), (1418995834.961524, 4185937283.90729)])
line3 = LineString([(1418996025.913674, 4185937224.432286), (1418998292.548948, 4185936518.443695)])
line4 = LineString([(1418998292.548684, 4185936518.443163), (1418998483.500807, 4185936458.968069)])
line5 = LineString([(1418995834.96857, 4185937283.930183), (1418996025.920693, 4185937224.455089)])
multiline = union_all([line1, line2, line3, line4, line5])

envelope = shapely.oriented_envelope(multiline)

plotting.plot_line(multiline)
plotting.plot_polygon(envelope, facecolor="none", color="red")
plt.show()

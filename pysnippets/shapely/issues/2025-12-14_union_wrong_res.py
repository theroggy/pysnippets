import os

import matplotlib.pyplot as plt
import shapely
from shapely import plotting

coords1 = [(-295.25030351249666, 4.236074061427525),
 (-295.08711234218333, -2.301948231163383),
 (-314.64218025800653, -2.7900491087570383),
 (-314.80537142831986, 3.7479731838338695)]
poly1 = shapely.Polygon(coords1)

coords2 = [(-275.69523559667346, 4.7241749390211805),
 (-275.53204442636013, -1.8138473535697273),
 (-295.08711234218333, -2.3019482311633825),
 (-295.25030351249666, 4.236074061427525)]
poly2 = shapely.Polygon(coords2)

print(f'{poly1.wkt=}')
print('poly1 area           ', poly1.area)
print(f'poly1 is_valid       {poly1.is_valid}')
print(f'{poly2.wkt=}')
print('poly2 area           ', poly2.area)
print(f'poly2 is_valid       {poly2.is_valid}')
print('incorrect union area ', shapely.union(poly1, poly2).area)
print(f'incorrect union is_valid {shapely.union(poly1, poly2).is_valid=}')
print(f"({(shapely.union(poly1, poly2).equals(poly2))=}")
print('incorrect union area ', shapely.unary_union(shapely.MultiPolygon([poly1, poly2])).area)
print('correct union area   ', shapely.union(poly1, poly2.buffer(0.00000000001)).area)

# Reproduce with geosop
geosop = "C:\\Tools\\miniforge3\\envs\\pysnippets\\Library\\bin\\geosop.exe"
cmdline = f'{geosop} -a "{shapely.MultiPolygon([poly1, poly2]).wkt}" unaryUnion'
print(f'Running command:\n{cmdline}\n')
os.system(cmdline)

# Plot
fig, ax = plt.subplots()
ax.set_title('Input Polygons')
ax.set_aspect("equal")
plotting.plot_polygon(ax=ax, polygon=poly1, color='blue', alpha=0.3)
plotting.plot_polygon(ax=ax, polygon=poly2, color='green', alpha=0.3)

union_incorrect = shapely.union_all([poly1, poly2])
plotting.plot_polygon(ax=ax, polygon=union_incorrect, color='purple', alpha=0.3)
plt.show()

import numpy as np
from shapely import LineString, MultiLineString, line_merge, union_all

geoms = [
	LineString([ (355041.15, 6688781.25, 0), (355040.9629213488, 6688781.437078651, 9.7) ]),
	LineString([ (355041.15, 6688781.25, 0), (354841.1500000001, 6688781.25, 0) ])
]

line_merge_result = line_merge(MultiLineString(geoms))
print(line_merge_result)
# LINESTRING Z (354841.1500000001 6688781.25 0, 355041.15 6688781.25 0, 355040.9629213488 6688781.437078651 9.7)

union_all_result = union_all(np.array(geoms))
print(union_all_result)
# MULTILINESTRING Z ((355041.15 6688781.25 0, 355040.9629213488 6688781.437078651 9.7), (355041.15 6688781.25 0, 354841.1500000001 6688781.25 0))

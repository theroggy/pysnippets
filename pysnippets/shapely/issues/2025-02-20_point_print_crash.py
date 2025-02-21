import numpy as np

from shapely.geometry import Point

import shapely

print(shapely.__version__)
print(shapely.geos_capi_version_string)

n = np.finfo(np.float32).max
p = Point(n, n)
print("Reaches")
print(p)
print("Reaches")

n = int(np.finfo(np.float64).max) - 1
p = Point(n, n)  # failure point
print("Reaches")  # @
print(p)
print("Doesn't reach")

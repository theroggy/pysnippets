"""
https://gis.stackexchange.com/questions/487165/merging-collinear-sides-a-k-a-deleting-collinear-vertices-of-a-polygon-or-lin/487183#487183
"""

import shapely as sh

p1 = sh.Polygon([(0,0),(1,0),(1,1),(0,1)])
p2 = sh.Polygon([(0,0),(2,0),(2,2)])
sum = sh.union(p1,p2)
sum_simplified = sh.simplify(sum, 0)

print(f"{sum=}")
print(f"{sum_simplified=}")

import os
from shapely import polygonize, from_wkt

wkt = 'LINESTRING (0 0 0 0, 0 1 1 1, 1 1 2 3, 1 0 4 5, 0 0 6 7)'
a = from_wkt(wkt)
print(a)
# <LINESTRING ZM (0 0 0 0, 0 1 1 1, 1 1 2 3, 1 0 4 5, 0 0 6 7)>
print(polygonize([a]))
# <GEOMETRYCOLLECTION Z (POLYGON Z ((0 0 0, 0 1 1, 1 1 2, 1 0 4, 0 0 6)))>

geosop = "C:\\Tools\\miniforge3\\envs\\pysnippets\\Library\\bin\\geosop.exe"
cmdline = f'{geosop} -a "{wkt}" polygonize'
print(cmdline)
os.system(cmdline)

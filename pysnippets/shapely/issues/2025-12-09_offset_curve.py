import os

import numpy as np
from shapely import LineString

outside = LineString(
    np.array(
        [
            [50.0, 0.0],
            [100.0, 0.0],
            [100.0, -100.0],
            [0.0, -100.0],
            [0.0, 0.0],
            [50.0 - 1e-9, 0.0],
        ]
    )
)
inside = outside.offset_curve(-5)

print(np.array(inside.coords))
print(inside.wkt)

geosop = "C:\\Tools\\miniforge3\\envs\\pysnippets\\Library\\bin\\geosop.exe"
wkt = outside.wkt
cmdline = f'{geosop} -a "{wkt}" offsetCurve N-5'
os.system(cmdline)

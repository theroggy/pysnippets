import numpy as np
import shapely.plotting
from matplotlib import pyplot as plt
from shapely import LineString

outside = LineString(
    np.array(
        [
            [50.0, 0.0],
            [100.0, 0.0],
            [100.0, -100.0],
            [0.0, -100.0],
            [0.0, 0.0],
            [0.0, 0.0],
            [50.0, 0.0],
        ]
    )
)
inside = outside.offset_curve(-5)

shapely.plotting.plot_line(outside)
shapely.plotting.plot_line(inside)
plt.show()

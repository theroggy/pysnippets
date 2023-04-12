import matplotlib.pyplot
import pygeoops
import shapely
import shapely.plotting

poly = shapely.Polygon(
    [
        [4095, 2660],
        [4035, 2660],
        [3956, 2666],
        [3881, 2678],
        [3810, 2695],
        [3740, 2718],
        [3656, 2748],
        [3601, 2771],
        [3710, 2767],
        [3722, 2763],
        [3803, 2736],
        [3870, 2719],
        [3946, 2704],
        [4017, 2697],
        [4098, 2695],
        [4095, 2660],
    ]
)

centerline = pygeoops.centerline(poly)
shapely.plotting.plot_polygon(poly)
shapely.plotting.plot_line(centerline)
matplotlib.pyplot.show()

import matplotlib.pyplot
import shapely
import shapely.plotting

poly = shapely.Polygon(
    shell=[(0, 0), (0, 80), (150, 0), (0, 0)],
    holes=[[(20, 30), (20, 31), (25, 30), (20, 30)]],
)
shapely.plotting.plot_polygon(poly)

poly_buf = shapely.buffer(
    poly, distance=-5, join_style=shapely.BufferJoinStyle.mitre, mitre_limit=1
)
shapely.plotting.plot_polygon(poly_buf)
matplotlib.pyplot.show()

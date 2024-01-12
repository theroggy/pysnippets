from matplotlib import pyplot as plt
import shapely
from shapely.ops import nearest_points


def snap2(g1, g2, threshold):
    coordinates = []
    for x, y in g1.coords:  # for each vertex in the first line
        point = shapely.Point(x, y)
        p1, p2 = nearest_points(point, g2)  # find the nearest point on the second line
        if p1.distance(p2) <= threshold:
            # it's within the snapping tolerance, use the snapped vertex
            coordinates.append(p2.coords[0])
        else:
            # it's too far, use the original vertex
            coordinates.append((x, y))
    # convert coordinates back to a LineString and return
    return shapely.LineString(coordinates)


from shapely.ops import snap
import shapely.plotting

square = shapely.Polygon([(1, 1), (1.5, 1), (2, 1), (2, 2), (1, 2), (1, 1)])
line = shapely.LineString([(0, 0), (0.8, 0.8), (1.8, 0.95), (2.6, 0.5)])
result = snap(line, square, 0.5)
print(result)

shapely.plotting.plot_polygon(square, color="blue")
shapely.plotting.plot_line(line, color="green")
shapely.plotting.plot_line(result, color="red")
plt.show()

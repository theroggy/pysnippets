import matplotlib.pyplot as plt
import shapely
import shapely.plotting

multi1 = shapely.MultiPolygon(
    [
        shapely.Polygon(shell=[(0, 0), (0, 5), (5, 5), (5, 0), (0, 0)]),
        shapely.Polygon(shell=[(10, 0), (15, 0), (15, 5), (10, 5), (10, 0)]),
    ]
)

multi2 = shapely.MultiPolygon(
    [
        shapely.Polygon(shell=[(0, 10), (5, 10), (5, 15), (0, 15), (0, 10)]),
        shapely.Polygon(shell=[(0, 20), (5, 20), (5, 25), (0, 25), (0, 20)]),
    ]
)

shapely.plotting.plot_polygon(multi1, color="red")
shapely.plotting.plot_polygon(multi2, color="blue")
plt.show()
print(f"distance: {multi2.distance(multi1)}")

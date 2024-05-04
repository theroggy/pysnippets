from matplotlib import pyplot as plt
from shapely import box
import shapely
import shapely.plotting as plot

room1 = box(20, 20, 40, 30)
room2 = box(40, 0, 50, 30)
house = shapely.union_all([room1, room2])

# Plot
plot.plot_polygon(room1, linewidth=6, facecolor="none")
plot.plot_polygon(room2, linewidth=6, facecolor="none")
plot.plot_polygon(house, linewidth=2, facecolor="none", color="red")

plt.show()

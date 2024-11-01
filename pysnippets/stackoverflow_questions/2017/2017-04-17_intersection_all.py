import matplotlib.pyplot as plt
import shapely
import shapely.plotting as plotter
from shapely import Point


coord1 = ( 0,0 )
point1 = Point(coord1)
circle1 = point1.buffer(1)

coord2 = ( 1,1 )
point2 = Point(coord2)
circle2 = point2.buffer(1)

coord3 = ( 1,0 )
point3 = Point(coord3)
circle3 = point3.buffer(1) 

intersection = shapely.intersection_all([circle1, circle2, circle3])

plotter.plot_polygon(circle1)
plotter.plot_polygon(circle2)
plotter.plot_polygon(circle3)
plotter.plot_polygon(intersection, color="red")
plt.show()

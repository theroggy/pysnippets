#!/usr/bin/python3
import numpy as np
import matplotlib.pyplot as plt
from shapely.geometry import Point, Polygon, LineString
from descartes import PolygonPatch

fig, ax = plt.subplots()

polygon = Polygon([[0.07, 0.0], [0.13, 0.0], [0.13, 0.04], [0.07, 0.04]])
patch = PolygonPatch(polygon, edgecolor='blue', facecolor='none', alpha=1.0)
ax.add_patch(patch)

line = LineString([(0.10,0.03), (0.14,0.03)])
ax.plot(*line.xy, color='black')

print("Intersection points <before> projection, Polygon.contains?")
interesection_points = np.array(polygon.boundary.intersection(line))
ax.plot(interesection_points[0], interesection_points[1], color='blue', marker='h', linestyle='', markersize=15, fillstyle='none', label='intersection before projection')
print (interesection_points, "contains:", polygon.touches(Point(interesection_points)))

print("Intersection points <after> projection, Polygon.contains?")
interesection_points_after_projection_case = polygon.boundary.intersection(line)
project_points = []
if not polygon.contains(interesection_points_after_projection_case):
    nearest_point = np.array(polygon.boundary.interpolate(polygon.boundary.project(interesection_points_after_projection_case)))
    project_points.append(nearest_point)
    print(nearest_point, "contains:", polygon.contains(Point(nearest_point)))

project_points = np.asarray(project_points)
ax.plot(project_points[:,0], project_points[:,1], color='green', marker='^', linestyle='', markersize=15, fillstyle='none', label='intersection after projection')

ax.legend()
plt.show()
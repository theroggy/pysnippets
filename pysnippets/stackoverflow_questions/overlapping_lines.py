from matplotlib import pyplot as plt
from shapely import LineString
from shapely.ops import transform
import shapely.plotting
from pyproj import CRS, Transformer

wgs84 = CRS('EPSG:4326')
utm = CRS('EPSG:32118')
project = Transformer.from_crs(wgs84, utm, always_xy=True).transform

rt1 = LineString([(-75.1949805258464, 40.07651359825427), (-75.20269373099198, 40.08091315230035) ])
rt2 = LineString([(-75.20130886000204, 40.080195561557595), (-75.2046746222474, 40.08211359104821 )])
rt3 = LineString([(-75.20052000948208, 40.08295187369251), (-75.20349134643484, 40.08478264710011)])

tot_length = {}
projected_routes = []
buffered_routes = []
routes = {'rt1': rt1, 'rt2': rt2, 'rt3': rt3}
for k in routes:
    route = routes[k]
    projected_route = transform(project, route)
    buffer = projected_route.buffer(10, cap_style="flat")
    projected_routes.append(projected_route)
    buffered_routes.append(buffer)

# Determine buffer intersections
buffer_intersections = []
for i, route1 in enumerate(buffered_routes):
    for j, route2 in enumerate(buffered_routes):
        if i == j:
            continue
        intersection = shapely.intersection(route1, route2)
        if not intersection.is_empty:
            buffer_intersections.append(intersection)

# Determine line intersections with buffer intersections
route_intersections = []
for route in projected_routes:
    for buffer in buffer_intersections:
        route_intersection = shapely.intersection(route, buffer)
        if not route_intersection.is_empty:
            route_intersections.append(route_intersection)

for line in projected_routes:
    shapely.plotting.plot_line(line)
for line in route_intersections:
    shapely.plotting.plot_line(line, color="red")
plt.show()

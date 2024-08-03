from matplotlib import pyplot as plt
import shapely
import shapely.plotting as plotter

pie_wkt = "POLYGON((16.00061 45.822171,15.99285240563651 45.8293452320342,15.990050859670909 45.82732350122485,15.988282915930574 45.82479740769603,15.987721633066801 45.82201422308267,15.988421953356983 45.8192463848863,16.00061 45.822171))"
pie = shapely.from_wkt(pie_wkt)

rect_wkt = (
    "POLYGON((15.989 45.82, 15.989 45.82, 15.989 45.82, 15.989 45.82, 15.989 45.82))"
)
rect = shapely.from_wkt(rect_wkt)
print(f"{rect.is_valid=}")

print(f"{shapely.intersects(pie, rect)=}")
print(f"{shapely.covers(pie, rect)=}")

fig, ax = plt.subplots()
plotter.plot_polygon(pie, ax=ax)
plotter.plot_polygon(rect, ax=ax, color="red")
plt.show()

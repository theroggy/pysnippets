import shapely

box = shapely.box(0, 0, 100, 100)
nb_lines = 0
for x in range(30, 200, 10):
    line = shapely.LineString([(x, 10), (x, 90)])
    if box.contains(line):
        nb_lines += 1
    else:
        break

print(f"nb_lines: {nb_lines}")

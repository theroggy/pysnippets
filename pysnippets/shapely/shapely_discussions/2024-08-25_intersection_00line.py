import shapely

poly = shapely.Polygon(
    [
        [-100, -100],
        [100, -150],
        [100, 100],
        [-100, 150],
    ]
)

line = shapely.LineString([[0, 0], [0, 0]])
print(f"{shapely.LineString([[0, 0], [0, 0]]).is_valid}")  # False

print(line.intersects(poly), poly.intersects(line))  # False, False

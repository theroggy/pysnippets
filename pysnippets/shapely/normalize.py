import shapely

coll = shapely.GeometryCollection(
    [
        shapely.box(0, 0, 10, 10),
        shapely.Point(50, 50),
        shapely.MultiPoint([(50, 50), (55, 55)]),
        shapely.LineString([(60, 60), (70, 70)]),
        shapely.box(-20, -20, -30, -30),
        shapely.box(20, 20, 30, 30),
        shapely.box(-30, 20, -20, 30),
        shapely.MultiLineString([[(60, 60), (70, 70)]]),
        shapely.box(20, -20, 30, -30),
        shapely.MultiLineString([[(60, 60), (70, 70)], [(80, 80), (90, 90)]]),
    ]
)
print(f"{str(coll)=}")
print(f"{str(coll.normalize())=}")

coll2 = shapely.GeometryCollection(
    [
        shapely.box(-30, 20, -20, 30),
        shapely.box(20, -20, 30, -30),
        shapely.box(20, 20, 30, 30),
        shapely.LineString([(60, 60), (70, 70)]),
        shapely.Point(50, 50),
        shapely.MultiPoint([(50, 50), (55, 55)]),
        shapely.box(0, 0, 10, 10),
        shapely.box(-20, -20, -30, -30),
        shapely.MultiLineString([[(60, 60), (70, 70)]]),
        shapely.MultiLineString([[(60, 60), (70, 70)], [(80, 80), (90, 90)]]),
    ]
)
print(f"{str(coll2)=}")
print(f"{str(coll2.normalize())=}")

import shapely

poly = shapely.box(2, 2, 8, 8)
collection = shapely.GeometryCollection(
    [
        shapely.box(0, 0, 5, 5),
        shapely.box(5, 0, 10, 5),
        shapely.box(0, 5, 5, 10),
        shapely.box(5, 5, 10, 10),
    ]
)
intersection = shapely.intersection(poly, collection)
print(intersection)

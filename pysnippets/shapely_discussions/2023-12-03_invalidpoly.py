import shapely
if __name__ == "__main__":
    a: shapely.Polygon = shapely.box(0,0,7,7)
    b: shapely.Polygon = shapely.box(1,1,10,10)
    c: shapely.Polygon = shapely.box(6,6,8,8)

    print(shapely.is_valid_reason(shapely.MultiPolygon([b,c])))
    # aa = shapely.intersection(a, shapely.MultiPolygon([b,c]))

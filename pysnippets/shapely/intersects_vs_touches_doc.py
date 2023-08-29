import shapely

poly1 = shapely.Polygon([(0,0), (10,0), (10,10), (0,10), (0,0)])
poly2 = shapely.Polygon([(0,0), (5,0), (5,10), (0,5), (0,0)])

print(f"intersects: {shapely.intersects(poly1, poly2)}")
print(f"touches: {shapely.touches(poly1, poly2)}")
print(f"within: {shapely.within(poly1, poly2)}")
print(f"overlaps: {shapely.overlaps(poly1, poly2)}")

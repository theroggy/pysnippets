from shapely import Point
import shapefile
from shapely.geometry import shape

w = shapefile.Writer("test", shapeType=5)
w.field("ID", "C", size=4)
w.field("Polygon", "C", size=15)
w.field("Descript", "C", size=40)

# Add Polygon A, the blue one, with 2 parts
w.poly(
    [
        [[0, 0], [0, 5], [5, 5], [5, 0], [0, 0]],  # poly 1, clockwise
        [[10, 10], [10, 20], [20, 20], [20, 10], [10, 10]],  # poly 2, clockwise
    ]
)
w.record(w.shpNum, "Polygon A", "Two separated squares (Aa and Ab)")


# Add Polygon B, the pink one, with one hole
w.poly(
    [
        [[40, 0], [40, 20], [60, 20], [60, 0], [40, 0]],  # poly 1, clockwise
        [[50, 10], [55, 10], [55, 15], [50, 15], [50, 10]],  # hole 1, counterclockwise
    ]
)
w.record(w.shpNum, "Polygon B", "Square with squared hole")

w.close()


# List of 4 points, the green ones, that I want to see if are inside Polygon A
test_points_1 = (
    Point(3, 3),  # Inside Polygon A, part Aa
    Point(6, 6),  # Outside Polygon A
    Point(15, 15),  # Inside Polygon A, part Ab
    Point(25, 25),  # Outside Polygon A
)

# List of 4 points, the black ones, that I want to see if are inside Polygon B
test_points_2 = (
    Point(45, 5),  # Inside Polygon B
    Point(52, 12),  # Outside Polygon B (inside hole)
    Point(58, 14),  # Inside Polygon B
    Point(65, 8),  # Outside Polygon B
)

#
# Open the shapefile, reads the points create a Polygon object with shapely and check
#

sfr = shapefile.Reader("test", encoding="iso8859-1")

# Test if points from test_points_1 are inside Polygon A
sr_1 = sfr.shapeRecords()[0]
poly = shape(sr_1.shape)
for pt in test_points_1:
    if pt.within(poly):
        print("Point ({0},{1}) is inside Polygon A".format(pt.x, pt.y))
    else:
        print("Point ({0},{1}) is outside Polygon A".format(pt.x, pt.y))

# Result:
# Point (3.0,3.0) is outside Polygon A     <-- Incorrect
# Point (6.0,6.0) is outside Polygon A     <-- Correct
# Point (15.0,15.0) is inside Polygon A    <-- Correct
# Point (25.0,25.0) is outside Polygon A   <-- Correct


# Test if points from test_points_2 are inside Polygon B
sr_2 = sfr.shapeRecords()[1]
poly = shape(sr_2.shape)
for pt in test_points_2:
    if pt.within(poly):
        print("Point ({0},{1}) is inside Polygon B".format(pt.x, pt.y))
    else:
        print("Point ({0},{1}) is outside Polygon B".format(pt.x, pt.y))

# Result
# Point (45.0,5.0) is outside Polygon B    <-- Incorrect
# Point (52.0,12.0) is outside Polygon B   <-- Correct
# Point (58.0,14.0) is inside Polygon B    <-- Correct
# Point (65.0,8.0) is outside Polygon B    <-- Correct

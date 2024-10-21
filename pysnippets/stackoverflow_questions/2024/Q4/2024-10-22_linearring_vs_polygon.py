"""
https://stackoverflow.com/questions/79111113/which-shapely-predicate-should-be-used-to-distinquish-between-these-linearrings/79111987#79111987
"""

from shapely import Polygon

# first use-case
blue_sq = Polygon([(1, 1), (1, 2), (2, 2), (2, 1), (1, 1)])
red_one = Polygon([(0, 0), (0, 3), (3, 3), (3, 2), (1, 2), (1, 0), (0, 0)])

print(f"{blue_sq.overlaps(red_one)=}")
print(f"{blue_sq.intersects(red_one)=}")
print(f"{blue_sq.crosses(red_one)=}")
print(f"{blue_sq.contains(red_one)=}")
print(f"{blue_sq.touches(red_one)=}")
print(f"{blue_sq.within(red_one)=}")

# second use-case
blue_ln = Polygon([(2, 1), (2, 2), (7, 2), (7, 1), (2, 1)])
red_two = Polygon([(1, 0), (1, 1), (2, 1), (2, 2), (3, 2), (3, 0), (1, 0)])

print(f"{blue_ln.overlaps(red_two)=}")
print(f"{blue_ln.intersects(red_two)=}")
print(f"{blue_ln.crosses(red_two)=}")
print(f"{blue_ln.contains(red_two)=}")
print(f"{blue_ln.touches(red_two)=}")
print(f"{blue_ln.within(red_two)=}")

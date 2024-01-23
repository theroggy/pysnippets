import shapely

points = [
    [175682.210293, 505233.365178],
    [175682.210295, 505233.365177],
    [175684.375108, 505254.524644],
    [175684.375109, 505254.524642],
    [175683.226468, 505243.284373],
]
print(f"points: {shapely.MultiPoint(points)}")
hull = shapely.concave_hull(
    shapely.MultiPoint(points)
)  # this crashes with "Process finished with exit code -1073741819 (0xC0000005)"
print("after hull")
print(f"hull: {hull}")

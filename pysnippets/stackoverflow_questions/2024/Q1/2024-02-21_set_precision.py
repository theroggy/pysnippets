import shapely

bbox = shapely.box(0, 0, 9, 9)
centroid = bbox.centroid
print(f"{centroid}")
# POINT (4.5 4.5)

centroid_rounded = shapely.set_precision(centroid, grid_size=1)
print(f"{centroid_rounded}")
# POINT (5 5)

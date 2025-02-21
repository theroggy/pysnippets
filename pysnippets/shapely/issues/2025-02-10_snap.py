from shapely import wkt, ops

box = wkt.loads(
    "LINEARRING (0 0, 0.16 0, 0.33 0, 0.5 0, 0.66 0, 0.83 0, 1 0, 1 0.16, 1 0.33, 1 0.5, 1 0.66, 1 0.83, 1 1, 0.83 1, 0.66 1, 0.5 1, 0.33 1, 0.16 1, 0 1, 0 0.83, 0 0.66, 0 0.5, 0 0.33, 0 0.16, 0 0)"
)
line = wkt.loads("LINESTRING (0.05 0.05, 0.95 0.95)")
snapped = ops.snap(line, box, 0.2)
print(snapped) # This should print a LineString going from [0,0] to [1,1], but it does not. 
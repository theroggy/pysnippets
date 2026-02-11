"""Interpolate a 3D line gives "wrong" results, or expected result isn't documented."""

from shapely import LineString

for line in [
    LineString([(0, 0, 0), (0, 0, 1), (0, 0, 2)]),
    LineString([(0, 0, 0), (0, 1, 1), (0, 2, 2)]),
]:
    for normalized in [True, False]:
        for dist in [0.5, 1]:
            result = line.interpolate(dist, normalized=normalized)
            print(f"interpolate {line=} ({line.length=}), {dist=}, {normalized=}: {result}")

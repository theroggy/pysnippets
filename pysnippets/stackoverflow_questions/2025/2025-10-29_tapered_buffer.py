"""Improve performance of variable distance buffer for polylines.

https://stackoverflow.com/questions/79804624/buffer-a-polyline-by-variable-distance
"""

import math
import time
from concurrent.futures import ProcessPoolExecutor
from itertools import batched, pairwise, repeat

import numpy as np
import matplotlib.pyplot as plt
import shapely
from pygeoops import buffer_by_m
from shapely import Point, convex_hull, MultiPoint, LineString, unary_union, Polygon
from shapely import plotting, LineString


def segment_buffer(p1, p2, dist1, dist2, quad_segs):
    poly1 = Point(p1).buffer(dist1, resolution=quad_segs)
    poly2 = Point(p2).buffer(dist2, resolution=quad_segs)
    return convex_hull(MultiPoint(np.concatenate([poly1.exterior.coords, poly2.exterior.coords])))


def variable_buffer(polyline: LineString, distances, quad_segs=16):
    pts = list(polyline.coords)
    parts = []
    for i in range(1, len(pts)):
        dist0 = distances[i - 1]
        dist1 = distances[i]
        if dist0 > 0 or dist1 > 0:
            poly = segment_buffer(pts[i - 1], pts[i], dist0, dist1, quad_segs=quad_segs)
            parts.append(poly)

    buffer_geom = unary_union(parts)

    if buffer_geom.is_empty:
        return Polygon()
    return buffer_geom


def buffer(navigation, distances, quad_segs=16):
    navigation = np.asarray(navigation)
    if not navigation.size:
        return Polygon()
    if len(navigation) != len(distances):
        raise ValueError("Number of points does not match number of distances")
    geometry = LineString(navigation)

    return variable_buffer(geometry, distances, quad_segs=quad_segs)


def variable_buffer2(polyline: LineString, distances, quad_segs=16):
    pts = shapely.points(shapely.get_coordinates(polyline))
    buffers = shapely.buffer(pts, distances, quad_segs=quad_segs)
    hull_inputs = [
        MultiPoint(shapely.get_coordinates([buffer1, buffer2]))
        for buffer1, buffer2 in pairwise(buffers)
    ]
    hulls = shapely.convex_hull(hull_inputs)
    buffer_geom = unary_union(hulls)

    if buffer_geom.is_empty:
        return Polygon()
    return buffer_geom


def buffer2(navigation, distances, quad_segs=16):
    navigation = np.asarray(navigation)
    if not navigation.size:
        return Polygon()
    if len(navigation) != len(distances):
        raise ValueError("Number of points does not match number of distances")
    geometry = LineString(navigation)

    return variable_buffer2(geometry, distances, quad_segs=quad_segs)


def buffer2_list(input_list: list[tuple]):
    result = [
        buffer2(navigation, distances, quad_segs)
        for navigation, distances, quad_segs in input_list
    ]
    return result

if __name__ == "__main__":

    line = [[0,0], [5,-2], [10,2], [15,0], [20,5], [25,0], [35, 0]]
    buffer_distances = [3, 4, 0, 2, 5, 2, 2]
    line_z = [[x, y, z]  for (x, y), z in zip(line, buffer_distances)]

    data = [(line, buffer_distances)] * 20000  # repeat to increase processing time
    data_z = [line_z] * 20000
    lines_z = [LineString(line) for line in data_z]

    quad_segs_orig = 16
    quad_segs_new = 8

    """
    # Single-threaded, original implementation
    # ----------------------------------------
    start = time.perf_counter()
    polygons = [buffer(*input, quad_segs_orig) for input in data]
    assert len(polygons) == len(data)
    print(f"Buffer, original, {quad_segs_orig=} took {time.perf_counter() - start:.4f} s")

    time.sleep(10)  # wait a moment to let system settle

    # Single-threaded, new implementation
    # -----------------------------------
    start = time.perf_counter()
    polygons = [buffer2(*input, quad_segs_orig) for input in data]
    assert len(polygons) == len(data)
    print(f"Buffer, new, {quad_segs_orig=} took {time.perf_counter() - start:.4f} s")

    time.sleep(10)  # wait a moment to let system settle
    """
    """
    # Single-threaded, new implementation
    # -----------------------------------
    start = time.perf_counter()
    polygons = [buffer2(*input, quad_segs_new) for input in data]
    assert len(polygons) == len(data)
    print(f"Buffer, new, {quad_segs_new=} took {time.perf_counter() - start:.4f} s")

    time.sleep(10)  # wait a moment to let system settle

    # Multi-threaded, new implementation
    # ----------------------------------
    start = time.perf_counter()
    # Split into batches
    n_workers = 8
    data_quadsegs = [(line, buffer_distances, 4) for line, buffer_distances in data]
    batches = batched(data_quadsegs, math.ceil(len(data_quadsegs) / n_workers))

    # Process in parallel
    with ProcessPoolExecutor(max_workers=n_workers) as executor:
        results = list(executor.map(buffer2_list, batches))

    polygons = np.concatenate(results)
    assert len(polygons) == len(data)
    print(f"Buffer, new, {quad_segs_new=}, {n_workers=} took {time.perf_counter() - start:.4f} s")

    # Single-threaded, pygeoops
    # -------------------------
    start = time.perf_counter()
    polygons = buffer_by_m(lines_z, quad_segs_new)
    assert len(polygons) == len(data)
    print(f"Buffer, pygeoops, {quad_segs_new=} took {time.perf_counter() - start:.4f} s")

    time.sleep(10)  # wait a moment to let system settle
    """

    # Multi-threaded, pygeoops
    # ------------------------
    start = time.perf_counter()
    # Split into batches
    n_workers = 8
    batches = list(batched(lines_z, math.ceil(len(lines_z) / n_workers)))

    # Process in parallel
    with ProcessPoolExecutor(max_workers=n_workers) as executor:
        results = list(executor.map(
            buffer_by_m, batches, repeat(quad_segs_new, len(batches))
        ))

    polygons = np.concatenate(results)
    assert len(polygons) == len(data)
    print(f"Buffer, pygeoops, {quad_segs_new=}, {n_workers=} took {time.perf_counter() - start:.4f} s")

    # Plot
    # ----
    fig, ax = plt.subplots()
    plotting.plot_polygon(polygons[0])
    plotting.plot_line(LineString(line))
    plt.show()

import shapely

# Tests if input is counter clockwise
p1_orig = shapely.Polygon([(0, 100), (0, 0), (100, 0), (100, 100)])
p1_set_prec = shapely.set_precision(p1_orig, grid_size=1e-3)
p1_orig_norm = shapely.normalize(p1_orig)
p1_set_prec_norm = shapely.normalize(p1_set_prec)
p1_inters_orig = shapely.intersection(p1_orig, p1_orig)
p1_inters_set_prec = shapely.intersection(p1_set_prec, p1_set_prec)
p1_inters_orig_norm = shapely.normalize(p1_inters_orig)

print(f"{p1_orig=} (counter-clockwise)")
print(f"{p1_set_prec=} (clockwise)")
print(f"{p1_orig_norm=} (clockwise)")
print(f"{p1_set_prec_norm=} (clockwise)")
print(f"{p1_inters_orig=} (clockwise)")
print(f"{p1_inters_set_prec=} (clockwise)")
print(f"{p1_inters_orig_norm=} (clockwise)")

# Tests if input is clockwise
p2_orig = shapely.Polygon([(0, 100), (100, 100), (100, 0), (0, 0)])
p2_inters_orig = shapely.intersection(p2_orig, p2_orig)

print(f"{p2_orig=} (clockwise)")
print(f"{p2_inters_orig=} (clockwise)")

# Tests on ordering of geometrycollections
l1_orig = shapely.LineString([(200, 100), (200, 0), (300, 0), (300, 100)])
c1_orig = shapely.GeometryCollection([p1_orig, l1_orig])
c1_inters = c1_orig.intersection(c1_orig.envelope)
print(f"c1_inters={c1_inters.wkt}")
c1_inters_norm = c1_inters.normalize()
print(f"c1_inters_norm={c1_inters_norm.wkt}")
c1_norm = c1_orig.normalize()
print(f"c1_norm={c1_norm.wkt}")

import shapely

p1_orig = shapely.geometry.Polygon([(0, 100), (0, 0), (100, 0), (100, 100)])
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

p2_orig = shapely.geometry.Polygon([(0, 100), (100, 100), (100, 0), (0, 0)])
p2_inters_orig = shapely.intersection(p2_orig, p2_orig)

print(f"{p2_orig=} (clockwise)")
print(f"{p2_inters_orig=} (clockwise)")

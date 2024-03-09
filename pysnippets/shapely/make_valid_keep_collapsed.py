import shapely

poly = shapely.from_wkt("MultiPolygon (((57479 202281, 57479 202259, 57454 202260, 57453 202277, 57479 202281),(57471 202270, 57471 202270, 57467 202270, 57471 202270)))")
print(f"{poly.is_valid=}")
poly_valid = shapely.make_valid(poly)
print(f"{poly_valid.is_valid=}")
print(f"{poly_valid.wkt=}")

import shapely

print(f"{shapely.geos_version=}")
polygon = shapely.from_wkt('POLYGON ((-90.7937622070313 30.4214403721742, -89.5001220703125 29.6439011074573, -90.0274658203125 29.5674849779702, -90.7937622070313 30.4214403721742))')
line = shapely.from_wkt('LINESTRING (-90.21896375277 30.004926101619, -90.21896375277 30.004926101619)')
point = shapely.from_wkt('POINT (-90.21896375277 30.004926101619)')
print(f"unprepared: {polygon.covers(line)=}, {polygon.covers(point)=}")
# GEOS 3.11.4?: (False, True)
# GEOS 3.13.0: unprepared: polygon.covers(line)=True, polygon.covers(point)=True
shapely.prepare(polygon)
print(f"prepared: {polygon.covers(line)=}, {polygon.covers(point)=}")
# GEOS 3.11.4?:  (True, True)
# GEOS 3.13.0: prepared: polygon.covers(line)=True, polygon.covers(point)=True

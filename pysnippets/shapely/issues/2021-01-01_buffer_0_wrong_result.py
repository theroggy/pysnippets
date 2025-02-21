import shapely.wkt

import urllib.request
with urllib.request.urlopen("https://github.com/Toblerity/Shapely/files/5845907/shape.txt") as f:
    wkt = f.read().decode("utf-8")

poly = shapely.wkt.loads(wkt)
print(f"{poly.is_valid=}") # prints True

print(f"{poly.equals(poly.buffer(0))=}") # prints True with GEOS 3.13.0

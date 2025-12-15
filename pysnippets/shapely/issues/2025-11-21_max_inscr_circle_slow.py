import time

import shapely

for a in [1e-6, 1e-7, 1e-13]:
    polygon = shapely.Polygon([(0.0, 0.0), (0.0, a), (12.0, a), (12.0, 0.0)])
    start = time.perf_counter()
    ic = shapely.maximum_inscribed_circle(polygon)
    print(f"Time taken: {time.perf_counter() - start:.6f} seconds")

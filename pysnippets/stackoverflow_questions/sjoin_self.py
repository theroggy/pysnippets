import geopandas as gpd
import numpy as np

# Buffer
gdf = gpd.read_file(gpd.datasets.get_path("nybb"))
buffer = gdf.copy()
buffer.geometry = buffer.geometry.buffer(3)

# Overlaps check
intersecting_gdf = buffer.sjoin(buffer, predicate="intersects")
intersecting_gdf = intersecting_gdf.loc[
    intersecting_gdf.index != intersecting_gdf.index_right
]
overlaps_ids = np.unique(intersecting_gdf.index)  # list overlapping IDs
print(overlaps_ids)

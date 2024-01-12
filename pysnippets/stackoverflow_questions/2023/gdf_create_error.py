import geopandas
import numpy as np
import shapely

carte = [
    [
        np.nan, np.nan, np.nan, np.nan, np.nan, 282.9896, np.nan, np.nan, 283.2407,
        283.2407, 282.73178, 282.63565, 282.63565, 282.73056, 282.81693, 282.81693,
        np.nan, np.nan, np.nan
    ],
    [
        np.nan, 283.01483, 282.85852, np.nan, np.nan, 282.84497, 282.78113, 282.78113,
        np.nan, np.nan, 282.75024, 282.75983, 282.75983, 282.97836, 283.19852,
        283.19852, 282.9773 , 282.9773, np.nan
    ],
    [
        np.nan, np.nan, np.nan, 282.63535, 282.63535, 282.70605, 282.7924, 282.7924,
        282.84875, 282.84875, 282.89798, 282.93933, 282.93933, 283.3523, 283.3246,
        283.3246, 283.08267, 283.08267, 282.97372
    ]
]

wkt = (
    "POLYGON ((51.39166666206273 4.083333332967527, 51.39166666206273 4.241666666286676, "
    "51.32499999540204 4.241666666286676, 51.32499999540204 4.083333332967527, "
    "51.39166666206273 4.083333332967527))"
)
geometry = shapely.from_wkt(wkt)
geometries = [geometry for _ in range(len(carte))]
map_gdf = geopandas.GeoDataFrame(carte, geometry=geometries, crs="EPSG:4326")
print(map_gdf)

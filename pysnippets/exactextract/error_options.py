import numpy as np

from exactextract import exact_extract
from exactextract.feature import JSONFeatureSource
from exactextract.raster import NumPyRasterSource


def make_rect(xmin, ymin, xmax, ymax, id=None, properties=None):
    f = {
        "type": "Feature",
        "geometry": {
            "type": "Polygon",
            "coordinates": [
                [[xmin, ymin], [xmax, ymin], [xmax, ymax], [xmin, ymax], [xmin, ymin]]
            ],
        },
    }

    if id is not None:
        f["id"] = id
    if properties is not None:
        f["properties"] = properties

    return f


rast = NumPyRasterSource(np.arange(1, 10, dtype=np.int32).reshape(3, 3))
square = JSONFeatureSource(make_rect(0.5, 0.5, 2.5, 2.5))
result = exact_extract(
    rast,
    square,
    [
        "m1=mean",
        "m2=mean(coverage_weight=area_spherical_m2)",
        "c1=coverage",
        "c2=coverage(coverage_weight=area_spherical_m2)",
        "c3=coverage(coverage_weight=area_spherical_km2)",
        "c4=coverage(coverage_weight=area_cartesian)",
    ],
    strategy="feature-sequential",
)[0]["properties"]

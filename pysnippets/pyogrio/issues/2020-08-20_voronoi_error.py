import pytest

from shapely.geos import geos_version
from shapely.wkt import loads as load_wkt

from shapely.ops import voronoi_diagram

requires_geos_35 = pytest.mark.skipif(
    geos_version < (3, 5, 0), reason="GEOS >= 3.5.0 is required."
)


@requires_geos_35
def test_from_multipoint_without_tolerace_with_floating_point_coordinates():
    mp = load_wkt(
        "MULTIPOINT (20.1273 18.7303, 26.5107 18.7303, 20.1273 23.8437, 26.5107 23.8437)"
    )

    regions = voronoi_diagram(mp)
    print("Len: %d -> Regions: %s" % (len(regions.geoms), str(regions)))


print(geos_version)
test_from_multipoint_without_tolerace_with_floating_point_coordinates()

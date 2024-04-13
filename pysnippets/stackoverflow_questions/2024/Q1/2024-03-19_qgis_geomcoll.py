import shapely
import geopandas as gpd

gpd.GeoSeries(
    [
        shapely.geometry.MultiLineString(
            [
                shapely.geometry.LineString([[0, 0], [0, 1]]),
                shapely.geometry.LineString([[1, 0], [1, 1]]),
            ]
        ),
        shapely.geometry.box(5, 5, 6, 6),
        shapely.geometry.Point(10, 10),
    ]
).set_crs(3857).to_file(
    "multi_type_test.gpkg", engine="pyogrio", geometry_type="Unknown"
)

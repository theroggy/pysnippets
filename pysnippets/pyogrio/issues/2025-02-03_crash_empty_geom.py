import geopandas
import pyogrio

df = geopandas.GeoDataFrame(
    {
        "geometry": geopandas.GeoSeries.from_wkt([
            "POLYGON EMPTY",
        ])
    }
)

df.to_file("foofy.fgb", layer_options={"SPATIAL_INDEX": "NO"})

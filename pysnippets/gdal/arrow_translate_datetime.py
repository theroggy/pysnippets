import warnings
from pathlib import Path
import geopandas as gpd
import pandas as pd
from osgeo import gdal
from shapely import Point

warnings.filterwarnings("ignore")
gdal.UseExceptions()

input_gdf = gpd.GeoDataFrame(
    data={
        "datetime_naive": pd.to_datetime(["2021-01-01 00:00:00", "2021-01-01 00:00:00", "2021-01-01 00:00:00"]),
        "datetime_utc": pd.to_datetime(["2021-01-01 00:00:00+00:00", "2021-01-01 00:00:00+00:00", "2021-01-01 00:00:00+00:00"]),
        "datetime_tz_local": pd.to_datetime(["2021-01-01 00:00:00+04:00", "2021-01-01 00:00:00+04:00", "2021-01-01 00:00:00+04:00"]),
        #"datetime_tz_mixed": pd.to_datetime(["2021-01-01 00:00:00+04:00", "2021-01-01 00:00:00+02:00", "2021-01-01 00:00:00+00:00"]),
    },
    geometry=[Point(0, 0), Point(0, 0), Point(0, 0)],
    crs=31370,
)

for suffix in [".gpkg", ".fgb"]:
    for arrow in ["YES", "NO"]:
        gdal.SetConfigOption("OGR2OGR_USE_ARROW_API", arrow)
        src = Path(f"C:/temp/src_arrow-{arrow}{suffix}")
        src.unlink(missing_ok=True)
        input_gdf.to_file(src)

        dst = Path(f"C:/temp/dst_arrow-{arrow}{suffix}")
        dst.unlink(missing_ok=True)
        ds_output = gdal.VectorTranslate(srcDS=src, destNameOrDestDS=dst)
        ds_output = None

        src_gdf = gpd.read_file(src)
        dst_gdf = gpd.read_file(dst)

        print(f"=== result for {suffix}, {arrow=} ===")
        print(src_gdf.drop(columns=["geometry"]))
        print(dst_gdf.drop(columns=["geometry"]))

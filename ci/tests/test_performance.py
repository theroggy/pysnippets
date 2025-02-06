import urllib.request
import warnings
from pathlib import PurePath
from time import perf_counter

from osgeo import gdal

gdal.UseExceptions()


def test_gdal_vectortranslate_performance(tmp_path):
    gfo_uri = "https://github.com/geofileops/geofileops/raw/refs/heads/main"
    remote_src = f"{gfo_uri}/tests/data/polygon-parcel.gpkg"
    src = tmp_path / "input.gpkg"
    dst = tmp_path / "output.gpkg"
    urllib.request.urlretrieve(remote_src, src)

    # Test!
    start = perf_counter()
    for i in range(1000):
        gdal.VectorTranslate(destNameOrDestDS=dst, srcDS=src)
        dst.unlink()
    
    elapsed = perf_counter() - start
    warnings.warn(f"Elapsed time: {elapsed}")


def test_gdal_openex_performance(tmp_path):
    gfo_uri = "https://github.com/geofileops/geofileops/raw/refs/heads/main"
    remote_src = f"{gfo_uri}/tests/data/polygon-parcel.gpkg"
    src = tmp_path / "input.gpkg"
    urllib.request.urlretrieve(remote_src, src)

    # Test!
    start = perf_counter()
    for i in range(10000):
        with gdal.OpenEx(str(src)) as ds:
            pass
    
    elapsed = perf_counter() - start
    warnings.warn(f"Elapsed time: {elapsed}")

import urllib.request
import warnings
from pathlib import PurePath
from time import perf_counter

import geofileops as gfo
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
        with gdal.OpenEx(str(src), gdal.OF_VECTOR) as ds:
            pass
    
    elapsed = perf_counter() - start
    warnings.warn(f"Elapsed time: {elapsed}")


def test_gfo_layerinfo_performance(tmp_path):
    gfo_uri = "https://github.com/geofileops/geofileops/raw/refs/heads/main"
    remote_src = f"{gfo_uri}/tests/data/polygon-parcel.gpkg"
    src = tmp_path / "input.gpkg"
    urllib.request.urlretrieve(remote_src, src)

    # Test!
    start = perf_counter()
    
    for i in range(10000):
        gfo.get_layerinfo(src)
    
    elapsed = perf_counter() - start
    warnings.warn(f"Elapsed time: {elapsed}")


def test_gfo_intersection_performance(tmp_path):
    gfo_uri = "https://github.com/geofileops/geofileops/raw/refs/heads/main"
    remote_src = f"{gfo_uri}/tests/data/polygon-parcel.gpkg"
    input1 = tmp_path / "input1.gpkg"
    urllib.request.urlretrieve(remote_src, input1)
    input2 = tmp_path / "input2.gpkg"
    gfo.copy(input1, input2)

    # Test!
    import cProfile, pstats, io
    from pstats import SortKey

    output = tmp_path / "output.gpkg"
    start = perf_counter()
    
    with cProfile.Profile() as pr:
        for i in range(10):
            gfo.intersection(input1, input2, output)
            output.unlink()

        s = io.StringIO()
        sortby = SortKey.CUMULATIVE
        ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
        ps.print_stats(30)
        print(s.getvalue())
        
    elapsed = perf_counter() - start
    warnings.warn(f"Elapsed time: {elapsed}")
    assert False

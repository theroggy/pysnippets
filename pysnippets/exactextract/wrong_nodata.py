from pathlib import Path

import numpy as np
import pytest
from numpy import nan
from osgeo import gdal

from exactextract import exact_extract

gdal.UseExceptions()


def create_gdal_raster(
    fname, values, *, gt=None, gdal_type=None, nodata=None, scale=None, offset=None
):
    gdal = pytest.importorskip("osgeo.gdal")
    gdal_array = pytest.importorskip("osgeo.gdal_array")
    drv = gdal.GetDriverByName("GTiff")
    bands = 1 if len(values.shape) == 2 else values.shape[0]
    if gdal_type is None:
        gdal_type = gdal_array.NumericTypeCodeToGDALTypeCode(values.dtype)
    ds = drv.Create(
        str(fname), values.shape[-2], values.shape[-1], bands=bands, eType=gdal_type
    )
    if gt is None:
        ds.SetGeoTransform((0.0, 1.0, 0.0, values.shape[-2], 0.0, -1.0))
    else:
        ds.SetGeoTransform(gt)
    if nodata:
        if type(nodata) in {list, tuple}:
            for i, v in enumerate(nodata):
                ds.GetRasterBand(i + 1).SetNoDataValue(v)
        else:
            ds.GetRasterBand(1).SetNoDataValue(nodata)
    if scale:
        ds.GetRasterBand(1).SetScale(scale)
    if offset:
        ds.GetRasterBand(1).SetOffset(offset)
    if len(values.shape) == 2:
        ds.WriteArray(values)
    else:
        for i in range(bands):
            ds.GetRasterBand(i + 1).WriteArray(values[i, :, :])


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


def test_tiff_nodata_scale_offset(tmp_path, gdal_type, nodata, offset, scale):
    print(
        "exact_extract for "
        f"gdal_type={gdal_type}, nodata={nodata}, scale={scale}, offset={offset}"
    )
    raster_fname = tmp_path / f"test_nodata_{offset}_{scale}.tif"
    raster_fname.unlink(missing_ok=True)
    raster_fname = str(raster_fname)
    create_gdal_raster(
        raster_fname,
        np.array(
            [
                [nodata, nodata, nodata],
                [nodata, nodata, nodata],
                [nodata, nodata, nodata],
            ]
        ),
        gdal_type=gdal_type,
        nodata=nodata,
        scale=scale,
        offset=offset,
    )
    square = make_rect(0, 0, 2, 2)

    results = exact_extract(raster_fname, square, "mode")

    # assert np.isnan(results[0]["properties"]["mode"])
    print(f"    -> {results=}")


if __name__ == "__main__":
    tmp_path = Path("C:/temp")

    # Test with nodata=2 and gdal_type=gdal.GDT_Byte
    test_tiff_nodata_scale_offset(
        tmp_path, gdal_type=gdal.GDT_Byte, nodata=2, scale=None, offset=None
    )
    # Test with nodata=nan and gdal_type=gdal.GDT_Float32
    test_tiff_nodata_scale_offset(
        tmp_path, gdal_type=gdal.GDT_Float32, nodata=np.nan, scale=None, offset=None
    )
    # Test with nodata=2 and gdal_type=gdal.GDT_Byte
    test_tiff_nodata_scale_offset(
        tmp_path, gdal_type=gdal.GDT_Byte, nodata=255, scale=0.004, offset=-0.08
    )
    # Test with nodata=nan and gdal_type=gdal.GDT_Float32
    test_tiff_nodata_scale_offset(
        tmp_path, gdal_type=gdal.GDT_Float32, nodata=np.nan, scale=0.004, offset=-0.08
    )

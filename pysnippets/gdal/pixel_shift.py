from pathlib import Path
from osgeo import gdal

gdal.UseExceptions()
tmp_dir = Path(__file__).parent / Path(__file__).stem
tmp_dir.mkdir(exist_ok=True)

# WMTS url
wmts_url = (
    "WMTS:https://geo.api.vlaanderen.be/omw/wmts/1.0.0/WMTSCapabilities.xml,"
    "layer=omwrgb23vl,"
    "tilematrixset=BPL72VL"
)

# Define the bounding box and projection window of the test roi
bbox = [174816, 176352, 175136, 176672]
projwin = [bbox[0], bbox[3], bbox[2], bbox[1]]

# Create a virtual raster file from the WMTS
input_vrt_path = tmp_dir / "input_vrt.vrt"
options = gdal.TranslateOptions(format="VRT", projWin=projwin)
gdal.Translate(input_vrt_path, wmts_url, options=options)

# Create a tif file from the WMTS
input_tif_path = tmp_dir / "input_tif.tif"
options = gdal.TranslateOptions(format="GTiff", projWin=projwin)
gdal.Translate(input_tif_path, wmts_url, options=options)

def translate_with_resample(input_path, projwin, width, height):

    # First method (fails when input_format is VRT)
    # There is a shift of about one pixel in the output
    output_direct_path = tmp_dir / f"{input_path.stem}_direct.tif"
    options = gdal.TranslateOptions(
        projWin=projwin, resampleAlg="nearest", width=width, height=height
    )
    gdal.Translate(output_direct_path, input_path, options=options)

    # Second method (works for both input_format)
    # There is no shift in the output
    # Here we first create a temporary tif file with the correct projection window
    # and then create the final output with the correct size
    output_indirect_tmp_path = tmp_dir / f"{input_path.stem}_indirect_temp.tif"
    options=gdal.TranslateOptions(projWin=projwin)
    gdal.Translate(output_indirect_tmp_path, input_path, options=options)

    output_indirect_path = tmp_dir / f"{input_path.stem}_indirect_result.tif"
    options=gdal.TranslateOptions(resampleAlg="nearest", width=width, height=height)
    gdal.Translate(output_indirect_path, output_indirect_tmp_path, options=options)


translate_with_resample(input_vrt_path, projwin, 1280, 1280)
translate_with_resample(input_tif_path, projwin, 1280, 1280)

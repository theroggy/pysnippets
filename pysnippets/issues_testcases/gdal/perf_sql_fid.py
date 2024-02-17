from datetime import datetime
from pathlib import Path
from osgeo import gdal

gdal.UseExceptions()

# Paths
src_orig = Path("C:/temp/prc2023.gpkg")
dst = "C:/temp/dst.gpkg"

# Run test
for ext in [".gpkg", ".shp", ".fgb"]:
    src = src_orig.parent / f"{src_orig.stem}{ext}"
    if not src.exists():
        ds_output = gdal.VectorTranslate(srcDS=str(src_orig), destNameOrDestDS=str(src))
        ds_output = None

    start = datetime.now()
    where = "fid IN (1, 100000, 500000)"
    options = gdal.VectorTranslateOptions(where=where)
    ds_output = gdal.VectorTranslate(srcDS=str(src), destNameOrDestDS=str(dst), options=options)
    ds_output = None

    print(f"for {ext}: took {datetime.now() - start}")

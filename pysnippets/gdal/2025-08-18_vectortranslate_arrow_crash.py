import shutil
import tempfile
from pathlib import Path

from osgeo import gdal
gdal.UseExceptions()


# Initialize input and output paths
input_url = "https://github.com/theroggy/pysnippets/raw/refs/heads/main/pysnippets/gdal/data/2025-08-18_vectortranslate_arrow_crash/"
output_dir = Path(tempfile.gettempdir()) / "vectortranslate_arrow_crash"
output_dir.mkdir(parents=True, exist_ok=True)

# Prepare src file that will be used to append
src_orig = f"{input_url}/deelkaart_6_integratie_makevalid_4.gpkg.zip"
src = output_dir / Path(src_orig).stem
if not src.exists():
    ds_output = gdal.VectorTranslate(srcDS=src_orig, destNameOrDestDS=src)
    ds_output = None
"""
src_limit = 55000
src = src_orig.with_name(f"{src_orig.stem}_{src_limit}.gpkg")
options = gdal.VectorTranslateOptions(limit=src_limit)
ds_output = gdal.VectorTranslate(srcDS=src_orig, destNameOrDestDS=src, options=options)
ds_output = None
"""

# Prepare initial destination file that will be used for appending to
dst_orig = f"{input_url}/deelkaart_6_integratie_makevalid_2000.gpkg.zip"
dst_start = output_dir / Path(dst_orig).stem
if not dst_start.exists():
    ds_output = gdal.VectorTranslate(srcDS=dst_orig, destNameOrDestDS=dst_start)
    ds_output = None

arrow = "YES"  # Change to "NO" to test without Arrow API
dst = output_dir / f"output_arrow-{arrow}.gpkg"
dst.unlink(missing_ok=True)

cpl_log_path = output_dir / "cpl_log.txt"
cpl_log_path.unlink(missing_ok=True)

gdal.SetConfigOption("OGR2OGR_USE_ARROW_API", arrow)
gdal.SetConfigOption("SPATIAL_INDEX", "NO")
gdal.SetConfigOption("OGR_SQLITE_CACHE", "128")
gdal.SetConfigOption("CPL_LOG_ERRORS", "ON")
gdal.SetConfigOption("CPL_DEBUG", "ON")
gdal.SetConfigOption("CPL_LOG", str(cpl_log_path))

for i in range(1000):
    print(f"Try appending nb {i} with arrow={arrow}...")
    if not dst.exists():
        print(f"Copy {dst}...")
        shutil.copy(src=dst_start, dst=dst)

    accessMode = "append" if dst.exists() else None

    options = gdal.VectorTranslateOptions(
        format="GPKG",
        layers=["deelkaart_6_integratie_makevalid"],
        layerName="deelkaart_6_integratie_makevalid",
        accessMode=accessMode,
        transactionSize=50_000,
    )
    ds_output = gdal.VectorTranslate(srcDS=src, destNameOrDestDS=dst, options=options)
    ds_output = None
    print(f"Appended nb {i} with arrow={arrow}")

    if i > 0 and i % 10 == 0:
        print(f"Remove {dst} to keep file size manageable")
        dst.unlink(missing_ok=True)

print("Ready")

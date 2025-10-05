import tempfile
from pathlib import Path

from osgeo import gdal

gdal.UseExceptions()

# Prepare test data
gfo_uri = "https://github.com/geofileops/geofileops/raw/refs/heads/main"
gpkg_path = f"/vsicurl/{gfo_uri}/tests/data/polygon-parcel.gpkg"
tmp_dir = Path(tempfile.gettempdir())
shp_path = tmp_dir / "polygon-parcel.shp"
ds = gdal.VectorTranslate(destNameOrDestDS=shp_path, srcDS=gpkg_path)
ds = None

clip_src = (156036, 196691, 156368, 196927)

# Clip the gpkg
gpkg_clipped_path = tmp_dir / "polygon-parcel-clipped.gpkg"
options = gdal.VectorTranslateOptions(clipSrc=clip_src)
ds = gdal.VectorTranslate(
    destNameOrDestDS=gpkg_clipped_path, srcDS=gpkg_path, options=options
)
layer = ds.GetLayer()
print(f"Number of features in clipped gpkg: {layer.GetFeatureCount()}")
ds = None

# Clip the shp
shp_clipped_path = tmp_dir / "polygon-parcel-clipped.shp"
options = gdal.VectorTranslateOptions(clipSrc=clip_src)
ds = gdal.VectorTranslate(
    destNameOrDestDS=shp_clipped_path, srcDS=shp_path, options=options
)
layer = ds.GetLayer()
print(f"Number of features in clipped shp: {layer.GetFeatureCount()}")
ds = None

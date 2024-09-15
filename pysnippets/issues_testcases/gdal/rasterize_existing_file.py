import shutil

from osgeo import gdal, ogr, osr

gdal.UseExceptions()

# Setup working spatial reference
# -------------------------------
# sr_wkt = 'LOCAL_CS["arbitrary"]'
# sr = osr.SpatialReference( sr_wkt )
sr = osr.SpatialReference()
sr.ImportFromEPSG(32631)
sr_wkt = sr.ExportToWkt()

# Create a test raster to add additional things to
# ------------------------------------------------

# Create a new raster to rasterize into.

path = r"C:\Temp\output.tif"

target_ds = gdal.GetDriverByName("GTiff").Create(path, 100, 100, 3, gdal.GDT_Byte)
target_ds.SetGeoTransform((1000, 1, 0, 1100, 0, -1))
target_ds.SetProjection(sr_wkt)

# Create a layer to rasterize from.

vector1_ds = gdal.GetDriverByName("Memory").Create("", 0, 0, 0)
vect1_lyr = vector1_ds.CreateLayer("vect1", srs=sr)

vect1_lyr.GetLayerDefn()
field_defn = ogr.FieldDefn("foo")
vect1_lyr.CreateField(field_defn)

# Add a polygon.

wkt_geom = "POLYGON((1020 1030,1020 1045,1050 1045,1050 1030,1020 1030))"

feat = ogr.Feature(vect1_lyr.GetLayerDefn())
feat.SetGeometryDirectly(ogr.Geometry(wkt=wkt_geom))

vect1_lyr.CreateFeature(feat)

ret = gdal.Rasterize(
    target_ds,
    vector1_ds,
    bands=[3, 2, 1],
    burnValues=[200, 220, 240],
    layers="vect1",
)
assert ret == 1

target_ds = None

# Add line to test raster via filepath
# ------------------------------------
via_filepath = r"C:\Temp\output_via_filepath.tif"
shutil.copy(path, via_filepath)

vector2_ds = gdal.GetDriverByName("Memory").Create("", 0, 0, 0)
vector2_lyr = vector2_ds.CreateLayer("vect2", srs=sr)

vector2_lyr.GetLayerDefn()
field_defn = ogr.FieldDefn("foo")
vector2_lyr.CreateField(field_defn)

# Add a linestring.

wkt_geom = "LINESTRING(1000 1000, 1100 1050)"

feat = ogr.Feature(vector2_lyr.GetLayerDefn())
feat.SetGeometryDirectly(ogr.Geometry(wkt=wkt_geom))

vector2_lyr.CreateFeature(feat)

try:
    ret = gdal.Rasterize(
        via_filepath,
        vector2_ds,
        bands=[3, 2, 1],
        burnValues=[200, 220, 240],
        layers="vect2",
    )
except Exception as ex:
    print(f"Error trying to write to filepath: {ex}")

# Add line to test raster after opening file
# ------------------------------------------
after_opening = r"C:\Temp\output_after_opening.tif"
shutil.copy(path, after_opening)

after_opening_ds = gdal.Open(after_opening, gdal.GA_Update)
ret = gdal.Rasterize(
    after_opening_ds,
    vector2_ds,
    bands=[3, 2, 1],
    burnValues=[200, 220, 240],
    layers="vect2",
)
assert ret == 1

# Check results.
expected = 6452
checksum = after_opening_ds.GetRasterBand(2).Checksum()
print(f"Expected result? {checksum == expected}")

after_opening_ds = None

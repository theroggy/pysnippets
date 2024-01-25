from osgeo import ogr, osr

memfile_path = "/vsimem/memoryfile.gpkg"
# memfile_path = "C:/temp/memoryfile.gpkg"
gpkg_ds = ogr.Open(memfile_path, update=1)

srs4326 = osr.SpatialReference()
srs4326.ImportFromEPSG(4326)
lyr = gpkg_ds.CreateLayer(
    "first_layer",
    geom_type=ogr.wkbPoint,
    srs=srs4326,
    options=["GEOMETRY_NAME=gpkg_geometry", "SPATIAL_INDEX=NO"],
)
assert lyr is not None

# Close file and open again

# Test creating a layer with an existing name
lyr = gpkg_ds.CreateLayer("a_layer", options=["SPATIAL_INDEX=NO"])
assert lyr is not None
with gdaltest.error_handler():
    lyr = gpkg_ds.CreateLayer("a_layer", options=["SPATIAL_INDEX=NO"])
assert lyr is None, "layer creation should have failed"

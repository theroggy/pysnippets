from osgeo import gdal, ogr

gdal.UseExceptions()

src = r"C:\Temp\polygon_parcel\polygon-parcel.tif"
output = r"C:\Temp\polygon_parcel\polygon-parcel_polygonized.shp"

# Open input
src_ds = gdal.Open(src)
srcband = src_ds.GetRasterBand(1)

# Create output shapefile
output_ds = ogr.GetDriverByName("ESRI Shapefile").CreateDataSource(output)
srs = src_ds.GetSpatialRef()
output_layer = output_ds.CreateLayer("output_layer", geom_type=ogr.wkbPolygon, srs=srs)
data_type = ogr.OFTInteger
if srcband.DataType in (gdal.GDT_Int64, gdal.GDT_UInt64):
    data_type = ogr.OFTInteger64
fd = ogr.FieldDefn("DN", data_type)
output_layer.CreateField(fd)

# Polygonize
gdal.Polygonize(srcBand=srcband, maskBand=None, outLayer=output_layer, iPixValField=0)

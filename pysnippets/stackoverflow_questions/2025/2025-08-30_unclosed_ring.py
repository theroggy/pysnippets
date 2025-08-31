import os
import geopandas as gpd
from osgeo import ogr, osr

driver = ogr.GetDriverByName("ESRI Shapefile")
out_path = "unclosed_polygon.shp"
if os.path.exists(out_path):
    driver.DeleteDataSource(out_path)

ds = driver.CreateDataSource(out_path)
srs = osr.SpatialReference()
srs.ImportFromEPSG(4326)

layer = ds.CreateLayer("unclosed_polygon", srs, ogr.wkbPolygon)
layer.CreateField(ogr.FieldDefn("id", ogr.OFTInteger))

# First polygon: unclosed ring (invalid)
ring1 = ogr.Geometry(ogr.wkbLinearRing)
for pt in [(0, 0), (0, 1), (1, 1), (1, 0)]:
    ring1.AddPoint(*pt)

poly1 = ogr.Geometry(ogr.wkbPolygon)
poly1.AddGeometry(ring1)

feat1 = ogr.Feature(layer.GetLayerDefn())
feat1.SetField("id", 1)
feat1.SetGeometry(poly1)
layer.CreateFeature(feat1)

# Second polygon: closed ring (valid)
ring2 = ogr.Geometry(ogr.wkbLinearRing)
for pt in [(2, 0), (2, 1), (3, 1), (3, 0), (2, 0)]:
    ring2.AddPoint(*pt)

poly2 = ogr.Geometry(ogr.wkbPolygon)
poly2.AddGeometry(ring2)

feat2 = ogr.Feature(layer.GetLayerDefn())
feat2.SetField("id", 2)
feat2.SetGeometry(poly2)
layer.CreateFeature(feat2)

# Cleanup
feat1 = None
feat2 = None
ds = None

gdf = gpd.read_file("unclosed_polygon.shp", on_invalid="fix")
print(gdf)

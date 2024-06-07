from osgeo import gdal

gdal.UseExceptions()

src = "https://www.ngi.be/tiles/arcgis/rest/services/seamless_carto__default__3857__140/MapServer?f=json"
dst = "output/XYZ_topo2.xml"

ds_output = gdal.Translate(srcDS=src, destName=dst, format="WMS")
ds_output = None

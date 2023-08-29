
from datetime import datetime
from osgeo import gdal
gdal.UseExceptions()

url = "/vsicurl/https://data.source.coop/cholmes/eurocrops/unprojected/flatgeobuf/FR_2018_EC21.fgb"

start = datetime.now()
datasource = gdal.OpenEx(url)
datasource_layer = datasource.GetLayer("FR_2018_EC21")
print(datasource_layer.GetExtent())
print(f"took {datetime.now() - start}")
datasource = None

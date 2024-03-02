import geopandas as gpd
from osgeo import gdal
import shapely

gdal.UseExceptions()

# Prepare test data
data = [
    {"descr": "point1", "geometry": shapely.MultiPoint([(0, 0)])},
    {"descr": "point2", "geometry": shapely.MultiPoint([(0, 1)])},
]
input_gdf = gpd.GeoDataFrame(data=data, crs=31370)
input_path = "/vsimem/input.gpkg"
input_gdf.to_file(input_path, engine="pyogrio", geometry_type="MultiPoint")
datasource = gdal.OpenEx(input_path)
datasource_layer = datasource.GetLayer(0)
geometrytype = gdal.ogr.GeometryTypeToName(datasource_layer.GetGeomType())
print(f"input geometrytype: {geometrytype}")
datasource = None

output_path = "/vsimem/output.gpkg"
options = gdal.VectorTranslateOptions(geometryType="Point")
gdal.VectorTranslate(destNameOrDestDS=output_path, srcDS=input_path, options=options)

datasource = gdal.OpenEx(output_path)
datasource_layer = datasource.GetLayer(0)
geometrytype = gdal.ogr.GeometryTypeToName(datasource_layer.GetGeomType())
print(f"output geometrytype: {geometrytype}")
datasource = None

output_gdf = gpd.read_file(output_path)
print(output_gdf)

output2_path = "/vsimem/output2.shp"
try:
    gdal.VectorTranslate(destNameOrDestDS=output2_path, srcDS=output_path)
except Exception as ex:
    print(f"VectorTranslate with sqlite sql statemement: Exception raised: {ex}")

output2_gdf = gpd.read_file(output2_path)
print(output2_gdf)

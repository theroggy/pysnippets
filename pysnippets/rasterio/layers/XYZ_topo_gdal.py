import geopandas as gpd
from osgeo import gdal
from shapely import box

gdal.UseExceptions()
roi = gpd.GeoDataFrame(
    geometry=[box(150000, 150000, 150250, 150250)], crs=31370
).to_crs(3857)
west, south, east, north = roi.total_bounds

options = gdal.TranslateOptions(projWin=f"{west}, {south}, {east}, {north}")
gdal.Translate(
    srcDS="rasterio/layers/XYZ_topo.xml",
    destName="output/read_XYZ_topo_output.jpg",
    options=options,
)

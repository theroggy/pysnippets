import geopandas as gpd
import matplotlib.pyplot as plt
from osgeo import gdal
import shapely.geometry

gdal.UseExceptions()

clip_bounds = [-1, 0, 2, 1]
clip_bbox = shapely.geometry.box(*clip_bounds)
options = gdal.VectorTranslateOptions(spatFilter=clip_bounds, clipSrc="spat_extent")

# Clip with arrow: no clipping occurs
line1 = gpd.GeoSeries(shapely.geometry.LineString([[0, 2], [0, -2], [2, -2]]))
line1_path = "line1.gpkg"
line1.to_file(line1_path, layer="line")
clipped1_arrow_path = "clipped_arrow.gpkg"
ds_output = gdal.VectorTranslate(
    srcDS=line1_path, destNameOrDestDS=clipped1_arrow_path, options=options
)
ds_output = None

# Clip without arrow: correct result
line2 = gpd.GeoSeries(shapely.geometry.LineString([[1, 2], [1, -1], [2, -1]]))
line2_path = "line2.gpkg"
line2.to_file(line2_path, layer="line")
with gdal.config_option("OGR2OGR_USE_ARROW_API", "NO"):
    clipped2_path = "clipped.gpkg"
    ds_output = gdal.VectorTranslate(
        srcDS=line2_path, destNameOrDestDS=clipped2_path, options=options
    )
    ds_output = None

# Plot, arrow
f, ax = plt.subplots()
line1_gdf = gpd.read_file(line1_path)
line2_gdf = gpd.read_file(line2_path)
clipped1_arrow_gdf = gpd.read_file(clipped1_arrow_path)
clipped2_gdf = gpd.read_file(clipped2_path)
line1_gdf.plot(color="red", ax=ax)
line2_gdf.plot(color="red", ax=ax)
gpd.GeoSeries(clip_bbox).plot(ax=ax, facecolor="none", edgecolor="blue")
clipped1_arrow_gdf.plot(ax=ax, color="green")
clipped2_gdf.plot(ax=ax, color="green")

plt.show()

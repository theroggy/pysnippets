from pathlib import Path

import geofileops as gfo
import geopandas as gpd
from osgeo import gdal


gdal.UseExceptions()

output = Path("C:/Temp/huge_points.gpkg")
output_noindex = output.with_stem(f"{output.stem}_noindex")

#output.unlink(missing_ok=True)
if not output_noindex.exists():
    for x in range(70):
        points = []
        for y in range(1_000_000):
            points.append((x, y))

        geometries = gpd.points_from_xy([p[0] for p in points], [p[1] for p in points])
        gdf = gpd.GeoDataFrame(geometry=geometries, crs=31370)
        gdf.to_file(output_noindex, append=True, spatial_index=False)

if not output.exists():
    gfo.copy(output_noindex, output)
    gfo.create_spatial_index(output, exist_ok=True)

output_noindex_zip = output_noindex.with_suffix(".gpkg.zip")
if not output_noindex_zip.exists():
    gdal.Run("vsi", "sozip", "create", input=output_noindex, output=output_noindex_zip)

output_zip = output.with_suffix(".gpkg.zip")
if not output_zip.exists():
    gdal.Run("vsi", "sozip", "create", input=output, output=output_zip)

# result = gdal.Run("vsi", "sozip", "list", input=output_zip)
# print(result.Output())

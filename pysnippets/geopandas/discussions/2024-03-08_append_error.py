import geopandas as gpd
from owslib.wfs import WebFeatureService

wfs = WebFeatureService("https://data.3dbag.nl/api/BAG3D/wfs", version="2.0.0")

response1 = wfs.getfeature(
    typename="BAG3D:lod12",
    bbox=(204000.00016165, 486000.00045928, 207000.0001644, 489000.00046109),
    method="Post",
    outputFormat="GML2",
    startindex=0,
    maxfeatures=500,
)

response2 = wfs.getfeature(
    typename="BAG3D:lod12",
    bbox=(204000.00016165, 486000.00045928, 207000.0001644, 489000.00046109),
    method="Post",
    outputFormat="GML2",
    startindex=500,
    maxfeatures=500,
)

gdf1 = gpd.read_file(response1)
gdf2 = gpd.read_file(response2)

print(all(gdf1.columns == gdf2.columns))  # True: Attributes are identical
print(all(gdf1.dtypes == gdf2.dtypes))  # True: Data types are identical

# In the second gdf, there is a row with an fid that already occurs in the first gdf.
# As the fid column is reused as a primary key in GPKG, error.
#gdf1 = gdf1.rename(columns={"fid": "fid_orig"})
#gdf2 = gdf2.rename(columns={"fid": "fid_orig"})
gdf1 = gdf1.set_index(["fid"])
gdf2 = gdf2.set_index(["fid"])

gdf1.to_file(
    "c:/temp/foo.gpkg", driver="GPKG", layer="Building", mode="w", engine="fiona"
)
gdf2.to_file(
    "c:/temp/foo.gpkg", driver="GPKG", layer="Building", mode="a", engine="fiona"
)  # Record does not match collection schema

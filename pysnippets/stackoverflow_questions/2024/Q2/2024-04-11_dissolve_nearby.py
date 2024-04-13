import geopandas as gpd
from matplotlib import pyplot as plt
import matplotlib.colors as mcolors

geojson_str = """{
    "type": "FeatureCollection",
    "features": [
    { "type": "Feature", "properties": { "Field1": 1, "Name": 1 }, "geometry": { "type": "Polygon", "coordinates": [ [ [ 13.39204563499591, 16.48343543977246, 0.0 ], [ 13.39204563499591, 10.0, 0.0 ], [ 10.0, 10.0, 0.0 ], [ 10.0, 16.48343543977246, 0.0 ], [ 13.39204563499591, 16.48343543977246, 0.0 ] ] ] } },
    { "type": "Feature", "properties": { "Field1": 2, "Name": 1 }, "geometry": { "type": "Polygon", "coordinates": [ [ [ 13.453358958249934, 23.292292286254376, 0.0 ], [ 13.453358958249934, 19.772218256233714, 0.0 ], [ 10.061313323254025, 19.772218256233714, 0.0 ], [ 10.061313323254025, 23.292292286254376, 0.0 ], [ 13.453358958249934, 23.292292286254376, 0.0 ] ] ] } },
    { "type": "Feature", "properties": { "Field1": 4, "Name": 1 }, "geometry": { "type": "Polygon", "coordinates": [ [ [ 17.117362156496036, 23.258050094611093, 0.0 ], [ 17.117362156496036, 17.975977362104913, 0.0 ], [ 13.725316521500124, 17.975977362104913, 0.0 ], [ 13.725316521500124, 23.258050094611093, 0.0 ], [ 17.117362156496036, 23.258050094611093, 0.0 ] ] ] } },
    { "type": "Feature", "properties": { "Field1": 1, "Name": 2 }, "geometry": { "type": "Polygon", "coordinates": [ [ [ 17.071320108878965, 12.848887677832408, 0.0 ], [ 17.071320108878965, 9.782661845158739, 0.0 ], [ 13.679274473883055, 9.782661845158739, 0.0 ], [ 13.679274473883055, 12.848887677832408, 0.0 ], [ 17.071320108878965, 12.848887677832408, 0.0 ] ] ] } },
    { "type": "Feature", "properties": { "Field1": 1, "Name": 5 }, "geometry": { "type": "Polygon", "coordinates": [ [ [ 9.663371858599694, 19.598706798419101, 0.0 ], [ 13.055417493595604, 19.598706798419101, 0.0 ], [ 13.055417493595604, 16.635345388667293, 0.0 ], [ 9.663371858599694, 16.635345388667293, 0.0 ], [ 9.663371858599694, 19.598706798419101, 0.0 ] ] ] } },
    { "type": "Feature", "properties": { "Field1": 1, "Name": 5 }, "geometry": { "type": "Polygon", "coordinates": [ [ [ 13.39204563499591, 16.48343543977246, 0.0 ], [ 13.39204563499591, 17.684798147038752, 0.0 ], [ 16.784091269991819, 17.684798147038752, 0.0 ], [ 16.784091269991819, 16.48343543977246, 0.0 ], [ 13.39204563499591, 16.48343543977246, 0.0 ] ] ] } },
    { "type": "Feature", "properties": { "Field1": 1, "Name": 5 }, "geometry": { "type": "Polygon", "coordinates": [ [ [ 17.15867000407675, 12.982990657533783, 0.0 ], [ 13.766624369080841, 12.982990657533783, 0.0 ], [ 13.766624369080841, 16.400200264632574, 0.0 ], [ 17.15867000407675, 16.400200264632574, 0.0 ], [ 17.15867000407675, 12.982990657533783, 0.0 ] ] ] } },
    { "type": "Feature", "properties": { "Field1": 4, "Name": 1 }, "geometry": { "type": "Polygon", "coordinates": [ [ [ 24.304485551158916, 27.21727245588152, 0.0 ], [ 24.304485551158916, 21.935199723375341, 0.0 ], [ 20.912439916163002, 21.935199723375341, 0.0 ], [ 20.912439916163002, 27.21727245588152, 0.0 ], [ 24.304485551158916, 27.21727245588152, 0.0 ] ] ] } },
    { "type": "Feature", "properties": { "Field1": 4, "Name": 1 }, "geometry": { "type": "Polygon", "coordinates": [ [ [ 27.759348375961771, 21.92149732297203, 0.0 ], [ 27.759348375961771, 16.63942459046585, 0.0 ], [ 24.367302740965862, 16.63942459046585, 0.0 ], [ 24.367302740965862, 21.92149732297203, 0.0 ], [ 27.759348375961771, 21.92149732297203, 0.0 ] ] ] } },
    { "type": "Feature", "properties": { "Field1": 1, "Name": 2 }, "geometry": { "type": "Polygon", "coordinates": [ [ [ 23.703648013427518, 14.664582009115662, 0.0 ], [ 23.703648013427518, 11.598356176441992, 0.0 ], [ 20.311602378431608, 11.598356176441992, 0.0 ], [ 20.311602378431608, 14.664582009115662, 0.0 ], [ 23.703648013427518, 14.664582009115662, 0.0 ] ] ] } },
    { "type": "Feature", "properties": { "Field1": 1, "Name": 2 }, "geometry": { "type": "Polygon", "coordinates": [ [ [ 27.133292861406996, 11.613206813486862, 0.0 ], [ 27.133292861406996, 8.546980980813192, 0.0 ], [ 23.741247226411087, 8.546980980813192, 0.0 ], [ 23.741247226411087, 11.613206813486862, 0.0 ], [ 27.133292861406996, 11.613206813486862, 0.0 ] ] ] } },
    { "type": "Feature", "properties": { "Field1": 1, "Name": 2 }, "geometry": { "type": "Polygon", "coordinates": [ [ [ 30.613373663033233, 8.561831617858058, 0.0 ], [ 30.613373663033233, 5.495605785184388, 0.0 ], [ 27.221328028037323, 5.495605785184388, 0.0 ], [ 27.221328028037323, 8.561831617858058, 0.0 ], [ 30.613373663033233, 8.561831617858058, 0.0 ] ] ] } },
    { "type": "Feature", "properties": { "Field1": 1, "Name": 5 }, "geometry": { "type": "Polygon", "coordinates": [ [ [ 27.766292424321669, 15.399062436367185, 0.0 ], [ 27.766292424321669, 16.600425143633476, 0.0 ], [ 31.158338059317579, 16.600425143633476, 0.0 ], [ 31.158338059317579, 15.399062436367185, 0.0 ], [ 27.766292424321669, 15.399062436367185, 0.0 ] ] ] } }
    ]
    }
"""
gdf = gpd.read_file(geojson_str, driver="GeoJSON")
max_distance = 0.5

# Apply buffering with half the distance so geometries within distance touch.
buffer_gdf = gdf.copy()
buffer_gdf["geometry"] = gdf.buffer(distance=max_distance / 2)

# Dissolve and explode, to find the clusters wanted.
buffer_dissolve_gdf = (
    buffer_gdf.dissolve(by=["Name"]).explode(index_parts=False).reset_index()
)
buffer_dissolve_gdf["cluster_id"] = buffer_dissolve_gdf.index

# Join the cluster id calculated to the original polygons.
clusters_gdf = gdf.sjoin(buffer_dissolve_gdf[["geometry", "cluster_id", "Name"]])
# Retain only those with matching Name.
clusters_gdf = clusters_gdf.loc[clusters_gdf["Name_left"] == clusters_gdf["Name_right"]]

# Dissolve on name and cluster_id
result_gdf = clusters_gdf.dissolve(by=["Name_left", "cluster_id"])

# Plot result
print(result_gdf)
c_list = [mcolors.TABLEAU_COLORS[c] for c in mcolors.TABLEAU_COLORS]
result_gdf.plot(color=c_list)
plt.show()

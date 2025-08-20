"""
Reference: https://stackoverflow.com/questions/79730009/how-to-read-a-geojson-file-when-an-attribute-column-values-are-lists-warningpy
"""

import geopandas as gpd

geojson = """{
    "type": "FeatureCollection",
    "name": "example",
    "crs": { "type": "name", "properties": { "name": "urn:ogc:def:crs:EPSG::3035" } },
    "features": [
        { "type": "Feature", "properties": { "tile_id": "tile-1", "paths": ["str1","str2" ] }, "geometry": { "type": "MultiPolygon", "coordinates": [ [ [ [ 5012847.978, 1927371.714 ], [ 5012847.978, 1929528.038 ], [ 5016147.973, 1929528.038 ], [ 5016147.973, 1927371.714 ], [ 5012847.978, 1927371.714 ] ] ] ] } }
    ]
}
"""

gdf = gpd.read_file(geojson, use_arrow=True)
print(gdf)

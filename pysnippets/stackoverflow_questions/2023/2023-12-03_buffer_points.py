from pathlib import Path
import json
import geopandas as gpd
from matplotlib import pyplot as plt
import shapely
from shapely import plotting

# Load geojson
with open(Path(__file__).with_suffix(".geojson")) as f:
    gj = json.load(f)

features = []
for f in gj["features"]:
    coords = f["geometry"]["coordinates"]
    print(coords[0][0])
    print(coords[0][1])
    print(tuple(coords[0]))
    print(coords)
    # quit()
    # Buffer points along line
    buffers = []
    for x, y, z in coords:
        buffer = gpd.points_from_xy([x], [y], crs=4326)
        buffer = buffer.to_crs(epsg=2163)
        buffer = buffer.buffer(2*1609.34)
        buffers.append(buffer)

    # Create multipolygon from buffers
    # mpolygon = shapely.MultiPolygon(buffers)
    mpolygon = shapely.union_all(buffers)
    plotting.plot_polygon(mpolygon)

    # Create feature
    features.append(
        {
            "geometry": gpd.GeoSeries(mpolygon).__geo_interface__,
            "properties": f["properties"],
        }
    )

# Output new GeoJSON
new_gj = {"type": "FeatureCollection", "features": features}

# output in .GeoJSON
with open("lines2Polygon.geojson", "w") as f:
    json.dump(new_gj, f)

print(new_gj)
plt.show()

import json
from matplotlib import pyplot as plt
import shapely
import shapely.plotting as plotter

geojson = {
    "type": "FeatureCollection",
    "name": "wrong",
    "crs": {"type": "name", "properties": {"name": "urn:ogc:def:crs:OGC:1.3:CRS84"} },
    "features": [{
        "type": "Feature",
        "properties": { "value": 98 },
        "geometry": {
            "type": "Polygon",
            "coordinates": [
                [[117.071654, 40.213989], [117.071654, 40.213965], [117.071643, 40.213956], [117.071643, 40.21394], [117.071632, 40.213932], [117.071632, 40.213915], [117.071621, 40.213907], [117.071621, 40.213883], [117.071611, 40.213875], [117.071611, 40.213858], [117.0716, 40.21385], [117.0716, 40.213834], [117.071589, 40.213825], [117.071589, 40.213801], [117.071579, 40.213793], [117.071579, 40.213784], [117.071568, 40.213776], [117.071546, 40.213776], [117.071536, 40.213784], [117.071514, 40.213784], [117.071514, 40.213686], [117.071525, 40.213678], [117.071525, 40.213563], [117.0716, 40.213563], [117.071611, 40.213555], [117.071697, 40.213555], [117.071707, 40.213547], [117.071697, 40.213539], [117.071697, 40.21353], [117.071675, 40.213514], [117.071782, 40.213514], [117.071804, 40.21353], [117.071815, 40.21353], [117.071847, 40.213555], [117.072244, 40.213555], [117.072244, 40.213752], [117.072093, 40.213752], [117.072083, 40.213743], [117.071911, 40.213743], [117.071879, 40.213768], [117.071868, 40.213768], [117.071847, 40.213784], [117.071664, 40.213784], [117.071654, 40.213793], [117.071654, 40.213989]]]  # fmt: skip # noqa: E501
        }
    }]
}

geom = shapely.from_geojson(json.dumps(geojson)).geoms[0]
print(f"{geom.is_valid}")

# Make the Polygon valid, and only retain the 0th geometry of the result, which is
# the Polygon. The 1st index is a Linestring.
geom_valid = shapely.make_valid(geom).geoms[0]

# Plot before and after
_, ax = plt.subplots()
plotter.plot_polygon(geom, ax=ax, color="red")
plotter.plot_polygon(geom_valid, ax=ax, color="green")
plt.show()

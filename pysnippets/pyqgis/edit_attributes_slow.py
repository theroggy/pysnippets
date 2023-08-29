from datetime import datetime
from pathlib import Path

import qgis.core  # type: ignore


layer_path = Path("C:/Temp/perc_2021_2022-02-02_copy.gpkg")
qgs = qgis.core.QgsApplication([], False)
qgs.initQgis()
layer = qgis.core.QgsVectorLayer(str(layer_path), layer_path.stem, "ogr")

"""
print("Start materialize to memory layer")
start = datetime.now()
layer_mem = layer.materialize(qgis.core.QgsFeatureRequest())
print(f"Materialize took {datetime.now()-start}")
del layer
layer = layer_mem
"""

print("Start layer.getFeatures() without update")
start = datetime.now()
print(f"layer.getFeatures() found {len(list(layer.getFeatures()))} features and took {datetime.now()-start}")

layer.startEditing()
print("Start loop to update features")
fieldid = layer.fields().indexFromName("GWSCOD_V")
start = datetime.now()
for feature in layer.getFeatures():
    layer.changeAttributeValue(feature.id(), fieldid, "test")
print(f"Loop took {datetime.now()-start}")

start = datetime.now()
layer.commitChanges()
print(f"Commitchanges took {datetime.now()-start}")

del layer

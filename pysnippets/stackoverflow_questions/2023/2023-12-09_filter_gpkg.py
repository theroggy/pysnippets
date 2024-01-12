import geopandas as gpd
data = dict()
i1 = "selected.txt"
f1 = open(i1, "r")
f1_select = f1.read()
data['osm'] = gpd.read_file('result_erase.gpkg', where = f1_select)
print(data['osm'])

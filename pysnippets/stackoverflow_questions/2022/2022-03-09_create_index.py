import geofileops as gfo

path = r"C:\Temp\lds-nz-building-outlines\nz-building-outlines.gpkg"
for layer in gfo.listlayers(path):
    gfo.create_spatial_index(path, layer, exist_ok=True)

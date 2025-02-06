from pathlib import Path
import geofileops as gfo
from osgeo import gdal


path = r"X:\GIS\GIS DATA\Ramsargebieden\ps_ramsar.gpkg"
dst_path = r"X:\GIS\GIS DATA\Ramsargebieden\ps_ramsar2.gpkg"
user_info_path = r"X:\GIS\GIS DATA\Ramsargebieden\ps_ramsar_13.gpkg"

print("------------------------------------")
print("Net voor get_layerinfo van origineel")
print("------------------------------------")
gfo.get_layerinfo(path)

if not Path(dst_path).exists():
    gdal.VectorTranslate(dst_path, path)

print("----------------------------------------------")
print("Net voor get_layerinfo van resultaat translate")
print("----------------------------------------------")
gfo.get_layerinfo(dst_path)

print("---------------------------------------------------")
print("Net voor get_layerinfo na pragma user_version=10300")
print("---------------------------------------------------")
gfo.get_layerinfo(user_info_path)

print("Klaar")

import os

os.system("ogrinfo --version")

path = r"C:\Temp\cosia\D075_2021_660_6870_vecto.gpkg"
os.system(f'ogrinfo "{path}"')

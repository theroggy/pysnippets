import geopandas as gpd
from matplotlib import pyplot as plt
import pandas as pd
from shapely import Point, Polygon
import shapely.plotting as pl

data = ['26-05-2022', '25-05-2024', 18, 'Acari', 'Ecorer', 40, -15.572136, -74.62736, 'Valid']
columns = ['Approval', 'Expiring', 'Zone', 'Project', 'Owner', 'Size(MW)', 'Latitude', 'Longitude', 'Status']
df = pd.DataFrame(data=[data], columns=columns)
geom = [Point(xy) for xy in zip(df['Latitude'],df['Longitude'])]
gdf = gpd.GeoDataFrame(df, crs='epsg:4326', geometry=geom)

data_ct = [
    ['A', 539953.3394,  8278356.7631,  '04-01-2022',  '04-01-2024',  18,  'Acari',  'ECORER',  40.0,  -15.572135812938946,  -74.62735981024672,  'Valid'],
    ['B',  543394.3582,  8278598.5842,  '04-01-2022',  '04-01-2024',  18,  'Acari',  'ECORER',  40.0,  -15.569892965187252,  -74.59527065391799,  'Valid'],
    ['C',  544374.9396,  8275284.2101,  '04-01-2022',  '04-01-2024',  18,  'Acari',  'ECORER',  40.0,  -15.599839630766777,  -74.58606516268479,  'Valid'],
    ['D',  545165.1468,  8272748.721,  '04-01-2022',  '04-01-2024',  18,  'Acari',  'ECORER',  40.0,  -15.622747690023045,  -74.57864734907821,  'Valid'],
    ['E',  544788.7396,  8271839.3717,  '04-01-2022',  '04-01-2024',  18,  'Acari',  'ECORER',  40.0,  -15.63097535601474,  -74.58214217679688,  'Valid'],
    ['F',  544531.8483,  8271218.7568,  '04-01-2022',  '04-01-2024',  18,  'Acari',  'ECORER',  40.0,  -15.636590561754735,  -74.58452749145272,  'Valid'],
    ['G',  544456.7666,  8271027.6721,  '04-01-2022',  '04-01-2024',  18, 'Acari',  'ECORER',  40.0,  -15.638319383853226,  -74.58522449548815,  'Valid'],
    ['H',  542762.6508,  8271564.0591,  '04-01-2022',  '04-01-2024',  18,  'Acari',  'ECORER',  40.0,  -15.6334994985371,  -74.60103947340889,  'Valid'],
    ['I',  539422.042,  8272621.7549,  '04-01-2022',  '04-01-2024',  18, 'Acari',  'ECORER',  40.0,  -15.623991822179361,  -74.63222276450333, 'Valid'],
    ['J',  539213.6429,  8272687.7377,  '04-01-2022',  '04-01-2024',  18,  'Acari',  'ECORER',  40.0,  -15.62339855055848,  -74.63416799727298, 'Valid'],
    ['K',  539093.1442,  8272725.8897,  '04-01-2022',  '04-01-2024',  18,  'Acari',  'ECORER',  40.0,  -15.623055506219488,  -74.63529274775954, 'Valid'],
    ['L',  538990.1647,  8272773.0558,  '04-01-2022',  '04-01-2024',  18, 'Acari',  'ECORER',  40.0,  -15.622630692945311,  -74.63625420113516, 'Valid'],
    ['M',  538932.8284,  8272868.6162,  '04-01-2022',  '04-01-2024',  18, 'Acari',  'ECORER',  40.0,  -15.621767660560035,  -74.63679061525991, 'Valid'],
    ['N',  538985.7452,  8273196.7002,  '04-01-2022',  '04-01-2024',  18, 'Acari',  'ECORER',  40.0,  -15.618800785309029,  -74.63630218613136, 'Valid'],
    ['O',  538687.323,  8273598.3445,  '04-01-2022',  '04-01-2024',  18,  'Acari',  'ECORER',  40.0,  -15.61517429311052,  -74.63909247921848, 'Valid'],
    ['P',  538678.0626,  8274064.0121,  '04-01-2022',  '04-01-2024',  18,  'Acari',  'ECORER',  40.0,  -15.610964542228787,  -74.63918622946272, 'Valid'],
    ['Q',  538924.4467,  8274264.8223,  '04-01-2022',  '04-01-2024',  18,  'Acari',  'ECORER',  40.0,  -15.609145320024819,  -74.63689102823527, 'Valid'],
    ['R',  538947.8091,  8275898.3227,  '04-01-2022',  '04-01-2024',  18,  'Acari',  'ECORER',  40.0,  -15.594377201030477,  -74.63669908037944,'Valid']
]

CT = pd.DataFrame.from_records(data=data_ct, columns=["ID", "X", "Y"] + columns)
CTP = CT[['Latitude', 'Longitude']]
polygon_geom = Polygon(zip(CTP['Latitude'],CTP['Longitude']))
# polygon_geom = Polygon(zip(CTP['Longitude'],CTP['Latitude']))
polygon = gpd.GeoDataFrame(index=[0], crs='epsg:4326', geometry=[polygon_geom])
polygonExport = polygon.sjoin(gdf, how='left')
print(polygonExport)

pl.plot_polygon(polygon_geom)
pl.plot_points(geom, color="red")
plt.show()
# polygon.to_file(filename=url + projectName + '.shp', driver="ESRI Shapefile")

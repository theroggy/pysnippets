import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt

proj4_string = (
    "+proj=lcc +lat_1=17.5 +lat_2=29.5 +lat_0=12 +lon_0=-102 +x_0=2500000 +y_0=0 "
    "+a=6378137 +rf=298.257222101 +units=m +no_defs"
)
mx = gpd.read_file("/content/enti.shp")
mx.crs = proj4_string
mx.plot()
print(mx)
print(mx.columns)

# Read the Excel data
excel_path = "/content/BH2020.xlsx"
df20 = pd.read_excel(excel_path)
merged_data = pd.merge(mx, df20, left_on="CVE_ENT_x", right_on="Entidades", how="left")

# Create the plot
merged_data.plot(
    column="TOTALES", cmap="Reds", linewidth=0.8, edgecolor="0.8", legend=True
)

# Set the title
plt.title("Brucelosis en México 2020")

# Show the plot
plt.show()

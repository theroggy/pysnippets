import geopandas as gpd
import topojson

#input_path = r"D:\EarthWorks\Algo\test_runs\SAOCOM\New folder\vectorize\EW_product_Vectorized_SM_layer.shp"
#output_path = r"D:\EarthWorks\Algo\test_runs\SAOCOM\New folder\vectorize\EW_product_Vectorized_SM_layer_douglas_peucker_50m_intersection.shp"

input_path = r"C:\Temp\polygon_parcel\polygon-parcel.gpkg"
output_path = r"C:\Temp\polygon_parcel\polygon-parcel_toposimpl.gpkg"

# Read the shapefile
input_gdf = gpd.read_file(input_path)

# Reproject to UTM
input_gdf = input_gdf.to_crs(32633)

# Convert to topology, simplify and convert back to GeoDataFrame
topo = topojson.Topology(input_gdf, prequantize=False)
topo_simpl = topo.toposimplify(0.5)
simpl_gdf = topo_simpl.to_gdf()

# Fix any invalid geometries (self-intersections)
simpl_gdf.geometry = simpl_gdf.geometry.make_valid()

# Reproject back to WGS84
simpl_gdf = simpl_gdf.to_crs(4326)

# Write to output file
simpl_gdf.to_file(output_path)

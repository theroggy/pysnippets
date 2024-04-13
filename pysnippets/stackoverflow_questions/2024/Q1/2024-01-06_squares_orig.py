from matplotlib import pyplot as plt
import numpy as np
import shapely
import geopandas as gpd


def define_spot_grid(gdf_base_grid, size_base, size_swath):
    """
    gdf_base_grid : our initial grid
    size_base     : size of the initial square
    size_swath    : size of our bigger square
    """

    rapport = size_swath/size_base
    unique_column = gdf_base_grid['column'].unique()
    unique_row = gdf_base_grid['row'].unique()
    liste_bigger_spot = []
    for k, v in gdf_base_grid.sort_values(by = ['row', 'column']).iterrows():
        # actually for every square i have a row and column information
        current_row, current_column = v['row'], v['column']
        bound_row, bound_column = v['row'] + rapport - 1, v['column'] + rapport - 1
        spot_bl = gdf_base_grid[(gdf_base_grid['row'] == current_row) & (gdf_base_grid['column'] == current_column)]
        spot_tl = gdf_base_grid[(gdf_base_grid['row'] == bound_row) & (gdf_base_grid['column'] == current_column)]
        spot_tr = gdf_base_grid[(gdf_base_grid['row'] == bound_row) & (gdf_base_grid['column'] == bound_column)]
        spot_br = gdf_base_grid[(gdf_base_grid['row'] == current_row) & (gdf_base_grid['column'] == bound_column)]
        # checking if all these squares exist
        if (not spot_bl.empty) and (not spot_tl.empty) and (not spot_tr.empty) and (not spot_br.empty):
            point_bl = spot_bl.unary_union.centroid
            point_tl = spot_tl.unary_union.centroid
            point_tr = spot_tr.unary_union.centroid
            point_br = spot_br.unary_union.centroid
            # we define a spot with 4 points
            bigger_spot = shapely.geometry.Polygon([point_bl, point_tl, point_tr, point_br])
            gdf_bigger_spot = gpd.GeoDataFrame({'geometry' : bigger_spot}, crs = 'epsg:4326', index = [0])
            # we check how many spot our bigger spot intersects using a spatial join
            sjoin = gpd.sjoin(gdf_bigger_spot, gdf_base_grid, how = 'right', predicate = 'intersects').dropna()
            # example : if rapport = 3 we need to get 9 squares, if it is less we do not keep
            if len(sjoin) == rapport**2:
                liste_bigger_spot.append(sjoin.unary_union)
    gdf_bigger = gpd.GeoDataFrame({'geometry' : liste_bigger_spot}, crs = 'epsg:4326', index = range(len(liste_bigger_spot)))
    return gdf_bigger

# Init parameters
size_base = 1

# Create base grid
a0 = shapely.geometry.Point([0, 0]).buffer(size_base / 2, cap_style="square")
a1 = shapely.affinity.translate(a0, xoff=1)
a2 = shapely.affinity.translate(a0, xoff=2)
a3 = shapely.affinity.translate(a0, xoff=3)
a4 = shapely.affinity.translate(a0, xoff=4)

b0 = shapely.affinity.translate(a0, yoff=1)
b1 = shapely.affinity.translate(b0, xoff=1)
b2 = shapely.affinity.translate(b0, xoff=2)
b3 = shapely.affinity.translate(b0, xoff=3)
b4 = shapely.affinity.translate(b0, xoff=4)

c0 = shapely.affinity.translate(b0, yoff=1)
c1 = shapely.affinity.translate(c0, xoff=1)
c2 = shapely.affinity.translate(c0, xoff=2)
c3 = shapely.affinity.translate(c0, xoff=3)

liste_geo = [a0, a1, a2, a3, a4, b0, b1, b2, b3, b4, c0, c1, c2, c3]
column = [1, 2, 3, 4, 5, 1, 2, 3, 4, 5, 1, 2, 3, 4]
row = [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 2, 2, 2, 2]

gdf_base_grid = gpd.GeoDataFrame(
    {"column": column, "row": row, "geometry": liste_geo},
    crs="epsg:4326",
    index=range(len(liste_geo)),
)

size_swath = size_base * 2
bigger_gdf = define_spot_grid(gdf_base_grid, size_base, size_swath)

# Plot result
f, ax = plt.subplots()
gdf_base_grid.plot(ax=ax, facecolor="none")
bigger_gdf.plot(ax=ax, facecolor="none", edgecolor="red", linewidth=2)
plt.show()

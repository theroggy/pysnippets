from matplotlib import pyplot as plt
import shapely
import shapely.plotting as plot

geom = shapely.from_wkt(
    "POLYGON ((1603268.502117987 6464060.781328565, 1603296.8217964454 6464047.851641227, 1603349.1085612718 6464035.338499875, 1603363.557831175 6464031.88480676, 1603361.0308787343 6464021.107210826, 1603317.7832565615 6463836.796863219, 1603217.2506244255 6463859.844110653, 1603202.3783404578 6463872.287568242, 1603157.794884393 6463914.581579376, 1603146.6963311615 6463924.630126579, 1603157.0490438067 6463936.205929175, 1603258.3275165292 6464049.413615812, 1603268.502117987 6464060.781328565))"
)
points = shapely.from_wkt(
    [
        "POINT (1603284.828798125 6464019.5353853395)",
        "POINT (1603323.0633351507 6464000.228348275)",
        "POINT (1603278.2522754562 6464030.13553264)",
        "POINT (1603304.896049631 6463958.075765142)",
        "POINT (1603264.5876622554 6463903.927670779)",
    ]
)
voronoi = shapely.get_parts(shapely.voronoi_polygons(shapely.union_all(points)))
clipped = shapely.intersection(voronoi, geom)
symmdiff = shapely.union_all(clipped).symmetric_difference(geom)
print(f"{symmdiff=}")
# output: symmdiff=<MULTIPOLYGON (...)>
print(f"{shapely.set_precision(symmdiff, 1e-8)=}")
# output: shapely.set_precision(symmdiff, 1e-8)=<MULTIPOLYGON EMPTY>

figure, ax = plt.subplots()
for voronoi_geom in voronoi:
    plot.plot_polygon(voronoi_geom, ax=ax, color="blue")
plot.plot_polygon(geom, ax=ax, color="green")
plt.show()

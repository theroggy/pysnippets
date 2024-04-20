    import geopandas as gpd
    import shapely


    # Test data
    sliver_width = 0.0001
    sliver = shapely.Polygon([(0, 0), (10, 0), (10, sliver_width), (0, 0)])
    poly = shapely.Polygon([(0 + sliver_width, 1), (10, 1), (10, 5), (0, 5), (0, 1)])
    gdf = gpd.GeoDataFrame(geometry=[sliver, poly])

    # Set precision with a grid_size ~10 times larger than the sliver width
    precision_gdf = gdf.copy()
    precision_gdf.geometry = shapely.set_precision(
        precision_gdf.geometry, grid_size=sliver_width * 10
    )
    filtered_gdf = gdf.loc[~precision_gdf.is_empty]

    print(f"Input\n{gdf}")
    print(f"Result of set_precision\n{precision_gdf}")
    print(f"Result of only filtering with set_precision\n{filtered_gdf}")

    # Output:
    # Input
    #                                             geometry
    # 0  POLYGON ((0.00000 0.00000, 10.00000 0.00000, 1...
    # 1  POLYGON ((0.00010 1.00000, 10.00000 1.00000, 1...
    # Result of set_precision
    #                                             geometry
    # 0                                      POLYGON EMPTY
    # 1  POLYGON ((0.00000 5.00000, 10.00000 5.00000, 1...
    # Result of only filtering with set_precision
    #                                             geometry
    # 1  POLYGON ((0.00010 1.00000, 10.00000 1.00000, 1...

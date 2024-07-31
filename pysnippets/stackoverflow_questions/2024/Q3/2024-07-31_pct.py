    import geopandas as gpd
    from shapely import box

    # vec_data = gpd.read_file("shapefile.shp")
    vec_data = gpd.GeoDataFrame(
        data={"class_name": ["forest", "road", "forest"]},
        geometry=[box(0, 0, 100, 100), box(100, 0, 110, 100), box(110, 0, 210, 100)],
    )
    vec_data["area"] = vec_data.area
    per_class = vec_data.groupby("class_name")[["area"]].sum()
    total_area = per_class["area"].sum()
    per_class["pct_area"] = per_class["area"] / total_area

    per_class.to_csv("vec_data2.csv")

    print(per_class)
    #                area  pct_area
    # class_name
    # forest      20000.0  0.952381
    # road         1000.0  0.047619

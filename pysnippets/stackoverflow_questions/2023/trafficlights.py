    import geopandas as gpd

    # Read your traffic light data
    lights = gpd.read_file("traffic_lights.gpkg")
    # Reproject to a projected crs, to be able to calculate distances <> degrees.
    lights_proj = lights.to_crs(epsg=32662)
    # Calculate buffer of 200 meter around each traffic light
    lights_buffer = lights_proj.buffer(200*0.3048)

    # Read your car data
    cars = gpd.read_file("cars.gpkg")
    # Reproject to a projected crs, to be compatible with you light data.
    cars_proj = cars.to_crs(epsg=32662)

    # Only keep the cars inside the traffic light buffers
    cars_in_lights_buffer = gpd.sjoin(cars_proj, lights_buffer)

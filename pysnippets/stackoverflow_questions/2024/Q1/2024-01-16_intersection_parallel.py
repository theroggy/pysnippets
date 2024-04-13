import geofileops as gfo

if __name__ == "__main__":
    # Shapefile is supported, but .gpkg will be faster
    input1_path = "input1.gpkg"
    input2_path = "input2.gpkg"
    output_path = "output.gpkg"

    gfo.intersection(
        input1_path=input1_path, input2_path=input2_path, output_path=output_path
    )

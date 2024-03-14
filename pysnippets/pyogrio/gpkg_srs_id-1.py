from pyproj import CRS

crs_undefined = CRS('LOCAL_CS["Undefined Cartesian SRS"]')
crs_undefined_unknown = CRS('LOCAL_CS["Undefined Cartesian SRS with unknown unit"]')
try:
    crs_undefined_unknown_eng = CRS(
        'ENGCRS["Undefined Cartesian SRS with unknown unit"]'
    )
except Exception as ex:
    print(f"Exception raised: {ex}")

crs_undefined_unknown_eng_wkt = """
    ENGCRS["Undefined Cartesian SRS with unknown unit",
        EDATUM["Unknown engineering datum"],
        CS[Cartesian,2],
            AXIS["X",unspecified,
                ORDER[1],
                LENGTHUNIT["unknown",0]],
            AXIS["Y",unspecified,
                ORDER[2],
                LENGTHUNIT["unknown",0]]]
"""
crs_undefined_unknown_eng2 = CRS(crs_undefined_unknown_eng_wkt)

# Check differences
print(f"{crs_undefined_unknown.equals(crs_undefined_unknown_eng2)=}")
print(f"{crs_undefined_unknown.to_wkt() == crs_undefined_unknown_eng2.to_wkt()=}")

print(f"{crs_undefined_unknown.equals(crs_undefined)=}")
print(f"{crs_undefined_unknown.to_wkt() == crs_undefined.to_wkt()=}")

print(f"{crs_undefined_unknown_eng2.equals(crs_undefined)=}")
print(f"{crs_undefined_unknown_eng2.to_wkt() == crs_undefined.to_wkt()=}")

"""Compare performance of reading with and without Arrow support in pyogrio."""

import time

import pyogrio

path = "C:/Temp/lds-nz-building-outlines/nz-building-outlines.gpkg"

for use_arrow in [True, False]:
    start_time = time.perf_counter()
    ds = pyogrio.read_dataframe(path, columns=[], use_arrow=use_arrow)
    took = time.perf_counter() - start_time
    print(f"use_arrow={use_arrow}: time={took:.4f} seconds")

import pyogrio

print(pyogrio.list_drivers())
print(f"{'DWG' in pyogrio.list_drivers()=}")
print(f"{'DXF' in pyogrio.list_drivers()=}")

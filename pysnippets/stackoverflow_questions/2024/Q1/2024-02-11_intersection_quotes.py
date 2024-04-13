import numpy as np
import pandas as pd
from shapely import LineString

dates = [
    1644796800000000000,
    1644883200000000000,
    1644969600000000000,
    1645056000000000000,
]
new50 = pd.DataFrame({"Date": dates, "Close": [np.nan, 410.0, 420.0, 500.0]})
new200 = pd.DataFrame({"Date": dates, "Close": [np.nan, 550.0, 500.0, 420.0]})

line1 = LineString(np.column_stack([new50.Close, new50.Date]))
line2 = LineString(np.column_stack([new200.Close, new200.Date]))
print(f"original: {line1.intersection(line2)}")

new50 = new50.dropna()
new200 = new200.dropna()

line1 = LineString(np.column_stack([new50.Close, new50.Date]))
line2 = LineString(np.column_stack([new200.Close, new200.Date]))
print(f"after dropna: {line1.intersection(line2)}")

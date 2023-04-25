import datetime
from rtree import index

# Prepare test data
x, y = (0, 0)
rects = []
size = 10
while y <= 10000:
    while x <= 10000:
        rects.append((x, y, x + size, y + size))
        x += size
    x = 0
    y += size

# Create rtree in bulk
start = datetime.datetime.now()
data = ((i, item, None) for i, item in enumerate(rects))
index_properties = index.Property(type=index.RT_RTree)
idx = index.Index(data, properties=index_properties)
print(f"create rtree took {datetime.datetime.now() - start}")

# Create rtree in loop
start = datetime.datetime.now()
data = ((i, item, None) for i, item in enumerate(rects))
index_properties = index.Property(type=index.RT_RTree)
idx = index.Index(properties=index_properties)
for id, rect in enumerate(rects):
    idx.insert(id=id, coordinates=rect)
print(f"create rtree took {datetime.datetime.now() - start}")

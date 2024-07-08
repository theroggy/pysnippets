import osmnx as ox

# Getting graph for specific road
cf = '["highway"!~"motorway"]["ref"~"TF-563"]'
G = ox.graph_from_place(
    "Tenerife, Spain", network_type="walk", simplify=False, custom_filter=cf
)

# Adding length weights
G = ox.distance.add_edge_lengths(G)

# Getting nodes and edges of graph
nodes, edges = ox.convert.graph_to_gdfs(G, nodes=True)

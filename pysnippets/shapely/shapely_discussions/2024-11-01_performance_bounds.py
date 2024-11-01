import time
import geopandas as gpd
import shapely

def calculate_overlap_score_orig(box1, box2, req_distance,
):
    """
    Calculate the overlap score between two rectangles based on their overlapping area,
    considering the required distance.

    Parameters:
    box1 : shapely.geometry
        The first rectangle object representing the boundary of a rectangle.
        
    box2 : shapely.geometry
        The second rectangle object representing the boundary of another rectangle.
        
    req_distance : float
        The specified minimum distance requirement. If the distance between the two rectangles 
        is less than this value, they are considered potentially overlapping.

    Returns:
    overlap_score : float
        Returns the calculated overlap score. If there is no overlap or the distance exceeds 
        the requirement, it returns 0.
    """
    
    # Axis-aligned quick filtering: calculate filter distance to ensure that if 
    # the distance exceeds this value on any axis, there is definitely no overlap.
    filter_distance = max(0, req_distance)  # Ensure that filter distance is non-negative

    # Manually expand the bounds of box1 based on the filter distance for subsequent overlap checks.
    expanded_minx = box1.bounds[0] - filter_distance  # Expanded minimum x coordinate
    expanded_miny = box1.bounds[1] - filter_distance  # Expanded minimum y coordinate
    expanded_maxx = box1.bounds[2] + filter_distance  # Expanded maximum x coordinate
    expanded_maxy = box1.bounds[3] + filter_distance  # Expanded maximum y coordinate

    # Use the expanded bounds to quickly filter out box2 if it's outside of box1's expanded bounds.
    if (expanded_maxx < box2.bounds[0] or expanded_maxy < box2.bounds[1] or
        expanded_minx > box2.bounds[2] or expanded_miny > box2.bounds[3]):
        return 0  # If there is no overlap, return 0

    overlap_score = 0  # Initialize overlap score
    current_distance = box1.distance(box2)  # Calculate the current distance between box1 and box2

    # If the current distance is less than or equal to the filter distance, there is potential overlap.
    if current_distance <= filter_distance:
        # Calculate score based on how close the current distance is to the required distance; 
        # closer distances yield higher scores.
        overlap_score += (filter_distance - current_distance) * 1
        
        # If the current distance is 0, it indicates that the two rectangles are completely overlapping.
        if current_distance == 0:  
            intersection = box1.intersection(box2)  # Calculate the intersection of both rectangles
            if not intersection.is_empty:  # If the intersection is not empty, add its area to the score
                overlap_score += intersection.area * 1
                
    return overlap_score  # Return the final calculated overlap score

def calculate_overlap_score_new(box1, box2, req_distance,
):
    """
    Calculate the overlap score between two rectangles based on their overlapping area,
    considering the required distance.

    Parameters:
    box1 : shapely.geometry
        The first rectangle object representing the boundary of a rectangle.
        
    box2 : shapely.geometry
        The second rectangle object representing the boundary of another rectangle.
        
    req_distance : float
        The specified minimum distance requirement. If the distance between the two rectangles 
        is less than this value, they are considered potentially overlapping.

    Returns:
    overlap_score : float
        Returns the calculated overlap score. If there is no overlap or the distance exceeds 
        the requirement, it returns 0.
    """
    
    # Axis-aligned quick filtering: calculate filter distance to ensure that if 
    # the distance exceeds this value on any axis, there is definitely no overlap.
    filter_distance = max(0, req_distance)  # Ensure that filter distance is non-negative

    # Manually expand the bounds of box1 based on the filter distance for subsequent overlap checks.
    # box1_bounds = shapely.bounds(box1)
    box1_coords = shapely.get_coordinates(box1)
    expanded_minx = box1_coords[:, 0].min().item() - filter_distance  # Expanded minimum x coordinate
    expanded_miny = box1_coords[:, 1].min().item() - filter_distance  # Expanded minimum y coordinate
    expanded_maxx = box1_coords[:, 0].max().item() + filter_distance  # Expanded maximum x coordinate
    expanded_maxy = box1_coords[:, 1].max().item() + filter_distance  # Expanded maximum y coordinate

    # Use the expanded bounds to quickly filter out box2 if it's outside of box1's expanded bounds.
    # box2_bounds = shapely.bounds(box2)
    box2_coords = shapely.get_coordinates(box2)
    if (expanded_maxx < box2_coords[:, 0].min().item() or expanded_maxy < box2_coords[:, 1].min().item() - filter_distance or
        expanded_minx > box2_coords[:, 0].max().item() or expanded_miny > box1_coords[:, 1].max().item()):
        return 0  # If there is no overlap, return 0

    overlap_score = 0  # Initialize overlap score
    current_distance = box1.distance(box2)  # Calculate the current distance between box1 and box2

    # If the current distance is less than or equal to the filter distance, there is potential overlap.
    if current_distance <= filter_distance:
        # Calculate score based on how close the current distance is to the required distance; 
        # closer distances yield higher scores.
        overlap_score += (filter_distance - current_distance) * 1
        
        # If the current distance is 0, it indicates that the two rectangles are completely overlapping.
        if current_distance == 0:
            intersection = box1.intersection(box2)  # Calculate the intersection of both rectangles
            if not intersection.is_empty:  # If the intersection is not empty, add its area to the score
                overlap_score += intersection.area * 1
                
    return overlap_score  # Return the final calculated overlap score

gdf = gpd.read_file(r"C:\Temp\prc2023\prc2023.gpkg", rows=400, use_arrow=True)
gdf.geometry = gdf.geometry.envelope
distance = 1

# Original implementation
start = time.perf_counter()
overlap_scores = []
for index, row1 in gdf.iterrows():
    for index, row2 in gdf.iterrows():
        overlap_scores.append(
            calculate_overlap_score_orig(row1.geometry, row2.geometry, distance)
        )
print(f"Elapsed time loop orig: {time.perf_counter() - start} seconds, {sum(overlap_scores)=}")
    
# Alternative implementation with minor optimalisation
start = time.perf_counter()
overlap_scores = []
for index, row1 in gdf.iterrows():
    for index, row2 in gdf.iterrows():
        overlap_scores.append(
            calculate_overlap_score_new(row1.geometry, row2.geometry, distance)
        )
print(f"Elapsed time loop new: {time.perf_counter() - start} seconds, {sum(overlap_scores)=}")

# Alternative implementation using spatial index
start = time.perf_counter()
tree = shapely.STRtree(gdf.geometry)
overlap_scores = []
buffers = gdf.geometry.buffer(distance, join_style="mitre").envelope
for index, row1 in gdf.iterrows():
    row1_geom_buffer = buffers[index]
    intersecting_idx = tree.query(row1_geom_buffer, predicate="intersects").tolist()

    # Calculate overlap score
    overlap_score = 0
    for idx in intersecting_idx:
        intersection = shapely.intersection(row1.geometry, gdf.geometry.iloc[idx])
        
        current_distance = shapely.distance(row1.geometry, gdf.geometry.iloc[idx])
        overlap_score += (distance - current_distance) * 1
        if not intersection.is_empty:            
            overlap_score += intersection.area * 1

    overlap_scores.append(overlap_score)

print(f"Elapsed time indexed: {time.perf_counter() - start} seconds, {sum(overlap_scores)=}")

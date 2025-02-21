from shapely.geometry import Point
from shapely.geometry import LineString
import matplotlib.pyplot as plt


def main():
    point = Point(15.068, 47.034)
    line = LineString(
        [
            (20.9927376195316, 64.8062322823664),
            (20.9603075300182, 64.6817017698049),
            (20.9603075300182, 64.6817017698049),  # duplicate point
        ]
    )

    # Check if the line is valid
    if not line.is_valid:
        raise ValueError("The line is not valid")

    if not line.is_simple:
        raise ValueError("The line is not valid")

    distance_on_line = line.project(point)

    print(distance_on_line)

    closest_point = line.interpolate(distance_on_line)

    _visualize_line_and_points(line, point, closest_point)


def _visualize_line_and_points(line, point, closest_point):

    line_x, line_y = line.xy
    point_x, point_y = point.xy
    closest_point_x, closest_point_y = closest_point.xy

    plt.figure(figsize=(10, 6))

    plt.plot(line_x, line_y, label="LineString")
    plt.scatter(point_x, point_y, color="red", label="Point")
    plt.scatter(closest_point_x, closest_point_y, color="blue", label="Point")

    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.title("Visualization of LineString and Point")
    plt.legend()
    plt.show()


if __name__ == "__main__":
    main()
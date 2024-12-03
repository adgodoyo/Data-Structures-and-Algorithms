from collections import namedtuple
from math import sqrt

Point = namedtuple('Point', 'x y')


def distance_squared(first_point, second_point):
    return (first_point.x - second_point.x) ** 2 + (first_point.y - second_point.y) ** 2


def closest_pair_recursive(points_sorted_x, points_sorted_y):
    if len(points_sorted_x) <= 3:
        min_distance = float('inf')
        for i in range(len(points_sorted_x)):
            for j in range(i + 1, len(points_sorted_x)):
                min_distance = min(min_distance, distance_squared(points_sorted_x[i], points_sorted_x[j]))
        return min_distance

    mid = len(points_sorted_x) // 2
    mid_point = points_sorted_x[mid]

    left_sorted_y = list(filter(lambda p: p.x <= mid_point.x, points_sorted_y))
    right_sorted_y = list(filter(lambda p: p.x > mid_point.x, points_sorted_y))

    d_left = closest_pair_recursive(points_sorted_x[:mid], left_sorted_y)
    d_right = closest_pair_recursive(points_sorted_x[mid:], right_sorted_y)
    d = min(d_left, d_right)

    strip = [p for p in points_sorted_y if abs(p.x - mid_point.x) ** 2 < d]

    min_strip_distance = float('inf')
    for i in range(len(strip)):
        for j in range(i + 1, len(strip)):
            if (strip[j].y - strip[i].y) ** 2 >= d:
                break
            min_strip_distance = min(min_strip_distance, distance_squared(strip[i], strip[j]))

    return min(d, min_strip_distance)


def minimum_distance_squared(points):
    points_sorted_x = sorted(points, key=lambda p: p.x)
    points_sorted_y = sorted(points, key=lambda p: p.y)
    return closest_pair_recursive(points_sorted_x, points_sorted_y)


if __name__ == '__main__':
    input_n = int(input())
    input_points = []
    for _ in range(input_n):
        x, y = map(int, input().split())
        input_point = Point(x, y)
        input_points.append(input_point)

    print("{0:.9f}".format(sqrt(minimum_distance_squared(input_points))))

from typing import NamedTuple, Tuple, List

import numpy as np
import re

rgx = 'position=<\s*(-?\d+),\s*(-?\d+)> velocity=<\s*(-?\d+),\s*(-?\d+)>'


class Point(NamedTuple):
    x_init: int
    y_init: int
    x_vel: int
    y_vel: int

    def get_pos(self, time: int) -> 'Point':
        return Point(
            self.x_init + time * self.x_vel,
            self.y_init + time * self.y_vel,
            self.x_vel,
            self.y_vel
        )

    def get_coord(self) -> Tuple[int, int]:
        return self.x_init, self.y_init

    def new_ref_point(self, x_min: int, y_min: int) -> 'Point':
        return Point(self.x_init - x_min, self.y_init - y_min, self.x_vel, self.y_vel)


def get_mins(list_of_points: List[Point]) -> Tuple[int, int]:
    x_min = np.inf
    y_min = np.inf
    for point in list_of_points:
        if point.x_init < x_min:
            x_min = point.x_init
        if point.y_init < y_min:
            y_min = point.y_init
    return x_min, y_min


def get_maxs(list_of_points: List[Point]) -> Tuple[int, int]:
    x_max = -np.inf
    y_max = -np.inf
    for point in list_of_points:
        if point.x_init > x_max:
            x_max = point.x_init
        if point.y_init > y_max:
            y_max = point.y_init
    return x_max, y_max


TEST_STRING = """position=< 9,  1> velocity=< 0,  2>
position=< 7,  0> velocity=<-1,  0>
position=< 3, -2> velocity=<-1,  1>
position=< 6, 10> velocity=<-2, -1>
position=< 2, -4> velocity=< 2,  2>
position=<-6, 10> velocity=< 2, -2>
position=< 1,  8> velocity=< 1, -1>
position=< 1,  7> velocity=< 1,  0>
position=<-3, 11> velocity=< 1, -2>
position=< 7,  6> velocity=<-1, -1>
position=<-2,  3> velocity=< 1,  0>
position=<-4,  3> velocity=< 2,  0>
position=<10, -3> velocity=<-1,  1>
position=< 5, 11> velocity=< 1, -2>
position=< 4,  7> velocity=< 0, -1>
position=< 8, -2> velocity=< 0,  1>
position=<15,  0> velocity=<-2,  0>
position=< 1,  6> velocity=< 1,  0>
position=< 8,  9> velocity=< 0, -1>
position=< 3,  3> velocity=<-1,  1>
position=< 0,  5> velocity=< 0, -1>
position=<-2,  2> velocity=< 2,  0>
position=< 5, -2> velocity=< 1,  2>
position=< 1,  4> velocity=< 2,  1>
position=<-2,  7> velocity=< 2, -2>
position=< 3,  6> velocity=<-1, -1>
position=< 5,  0> velocity=< 1,  0>
position=<-6,  0> velocity=< 2,  0>
position=< 5,  9> velocity=< 1, -2>
position=<14,  7> velocity=<-2,  0>
position=<-3,  6> velocity=< 2, -1>
"""

TEST = [Point(*list(map(int, re.match(rgx, s).groups())))
        for s in TEST_STRING.strip().split('\n')]
TEST_recalibrate = [point.new_ref_point(*get_mins(TEST)) for point in TEST]

x_max, y_max = get_maxs(TEST_recalibrate)

with open('./data/day10_input.txt', 'r') as f:
    inputs = [line.strip() for line in f.readlines()]

list_of_points = [Point(*list(map(int, re.match(rgx, s).groups())))
                  for s in inputs]


def get_area(list_of_points: List[Point]) -> int:
    x_max, y_max = get_maxs(list_of_points)
    x_min, y_min = get_mins(list_of_points)

    return (x_max - x_min) * (y_max - y_min)


for i in range(10500, 10700):
    time = i
    curr_pos = [point.get_pos(time) for point in list_of_points]
    print(time, get_area(curr_pos))

# Minimum: 10605
final_points = [point.get_pos(10605) for point in list_of_points]

x_max, y_max = get_maxs(final_points)
x_min, y_min = get_mins(final_points)
x_range = x_max - x_min
y_range = y_max - y_min

final_points_set = set([point.get_coord() for point in final_points])

grid = '\n'.join([''.join(['#' if (x, y) in final_points_set else '.' for x in range(
    x_min, x_max + 1)]) for y in range(y_min, y_max + 1)])

print(grid)

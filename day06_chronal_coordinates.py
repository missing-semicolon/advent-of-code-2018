from typing import NamedTuple, List, Tuple, Dict
from collections import Counter


Point = Tuple[int, int]


class coordinate(NamedTuple):
    name: int
    r: int
    d: int

    def get_coord(self) -> Tuple[int, int]:
        return (self.r, self.d)

    def get_distance(self, point: Tuple[int, int]) -> int:
        return abs(self.r - point[0]) + abs(self.d - point[1])


TEST_COORDS = """1, 1
1, 6
8, 3
3, 4
5, 5
8, 9
"""


def load_data() -> str:
    with open('./data/day06_input.txt', 'r') as f:
        return f.read()


def parse_coods(coord_txt: str) -> List[coordinate]:
    coord_list = [r.split(', ') for r in coord_txt.strip().split('\n')]
    return [
        coordinate(i, int(r[0]), int(r[1])) for i, r in enumerate(coord_list)
    ]


def get_max_coords(list_of_coords: List[coordinate]) -> Point:
    max_r = sorted([coord.get_coord()[0] for coord in list_of_coords])[-1] + 1
    max_d = sorted([coord.get_coord()[1] for coord in list_of_coords])[-1] + 1
    return max_r, max_d


def get_max_finite_area(coordinate_labels: Dict[Point, int], max_r: int, max_d: int) -> List[int]:  # noqa: E501
    infinite_labels = set()
    # left / right sides
    for d in range(max_d):
        infinite_labels.add(coordinate_labels[(0, d)])
        infinite_labels.add(coordinate_labels[(max_r - 1, d)])
    # top / bottom
    for r in range(max_r):
        infinite_labels.add(coordinate_labels[r, 0])
        infinite_labels.add(coordinate_labels[r, max_d - 1])

    areas = Counter(coordinate_labels.values())
    areas_no_infinite = [
        v for k, v in areas.items() if k not in infinite_labels and k is not None]  # noqa: E501
    return areas_no_infinite


def create_coordinate_labels(list_of_coords):  # noqa: E501
    coordinate_labels = dict()
    max_r, max_d = get_max_coords(list_of_coords)

    for r in range(max_r):
        for d in range(max_d):
            distances = sorted([(coord.get_distance((r, d)), i)
                                for i, coord in enumerate(list_of_coords)])

            if distances[0][0] != distances[1][0]:  # If no distance tie
                closest_dist, closest_name = distances[0]
                coordinate_labels[(r, d)] = closest_name
            else:
                coordinate_labels[(r, d)] = None
    return coordinate_labels


def find_safe_region_size(list_of_coords: List[coordinate], distance_thresh: int) -> int:  # noqa: E501
    coordinate_labels = dict()
    max_r, max_d = get_max_coords(list_of_coords)

    for r in range(max_r):
        for d in range(max_d):
            distances = [coord.get_distance((r, d))
                         for coord in list_of_coords]

            if sum(distances) <= distance_thresh:
                coordinate_labels[(r, d)] = sum(distances)
    return len(coordinate_labels.keys())


test_coord_list = parse_coods(TEST_COORDS)
max_r, max_d = get_max_coords(test_coord_list)
coordinate_labels = create_coordinate_labels(test_coord_list)
assert max(get_max_finite_area(coordinate_labels, max_r, max_d)) == 17

assert find_safe_region_size(test_coord_list, 30) == 16


assert coordinate_labels[(0, 0)] == 0
assert coordinate_labels[(5, 0)] is None

# Solution 1
raw_in = load_data()
coord_list = parse_coods(raw_in)
max_r, max_d = get_max_coords(coord_list)
coordinate_labels = create_coordinate_labels(coord_list)
assert all([coordinate_labels[(c.r, c.d)] == c.name for c in coord_list])
print(max(get_max_finite_area(coordinate_labels, max_r, max_d)))

# Solution 2
print(find_safe_region_size(coord_list, 10000))

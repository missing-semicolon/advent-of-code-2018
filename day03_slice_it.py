"""
https://adventofcode.com/2018/day/3
"""

from itertools import product
from collections import Counter


def load_file():
    with open('./day03_input.txt', 'r') as file:
        raw_lines = [line.strip() for line in file.readlines()]
    return raw_lines


def parse_slices(raw_in):
    list_of_slices = list()
    for line in raw_in:
        slice_id, pattern = line.split(' @ ')
        slice_id = int(slice_id[1:])

        origin, size = pattern.split(': ')
        origin = tuple([int(x) for x in origin.split(',')])
        size = tuple([int(x) for x in size.split('x')])
        list_of_slices.append(tuple([slice_id, origin, size]))

    return list_of_slices


assert parse_slices(["#123 @ 3,2: 5x4"]) == [(123, (3, 2), (5, 4))]


def get_coords_for_slice(slice_in):
    slice_id = slice_in[0]
    left_origin = slice_in[1][0]
    top_origin = slice_in[1][1]
    width = slice_in[2][0]
    height = slice_in[2][1]
    x_list = [x for x in range(left_origin, left_origin + width)]
    y_list = [y for y in range(top_origin, top_origin + height)]

    return {'slice_id': slice_id, 'coords': [x for x in product(x_list, y_list)]}


def find_overlaps(list_of_slices):
    slice_counter = Counter()
    for slice_in in list_of_slices:
        slice_coord_list = get_coords_for_slice(slice_in)
        for slice_coord in slice_coord_list.get('coords'):
            slice_counter[slice_coord] += 1

    return slice_counter


def count_overlaps(slice_counter):
    return len([x for x in slice_counter.values() if x > 1])


TEST_LIST = [
    "#1 @ 1,3: 4x4",
    "#2 @ 3,1: 4x4",
    "#3 @ 5,5: 2x2",
]

assert count_overlaps(find_overlaps(parse_slices(TEST_LIST))) == 4


def get_unique_claim(list_of_slices):
    counts = find_overlaps(list_of_slices)
    clean_slices = list()
    for slice_in in list_of_slices:
        slice_dict = get_coords_for_slice(slice_in)
        coords = slice_dict.get('coords')
        if (all(counts[coord] == 1 for coord in coords)):
            clean_slices.append(slice_dict['slice_id'])
    assert len(clean_slices) == 1
    return clean_slices[0]


# assert get_unique_claim(parse_slices(TEST_LIST)) == {3}


if __name__ == '__main__':
    raw_in = load_file()
    list_of_slices = parse_slices(raw_in)
    overlaps = find_overlaps(list_of_slices)
    print(count_overlaps(overlaps))
    print(get_unique_claim(list_of_slices))

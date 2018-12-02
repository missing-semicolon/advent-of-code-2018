"""
https://adventofcode.com/2018/day/2
"""


def create_list_of_boxes():
    list_of_boxes = list()
    with open('./day02_input.txt', 'r') as f:
        for line in f:
            list_of_boxes.append(line)
    return list_of_boxes


def create_checksum(list_of_boxes):
    counter_2 = 0
    counter_3 = 0

    for box in list_of_boxes:
        has_two, has_three = check_for_repeats(box)

        if has_two:
            counter_2 += 1

        if has_three:
            counter_3 += 1

    return counter_2 * counter_3


def check_for_repeats(box):
    counter = dict()
    for char in box:
        if char in counter.keys():
            counter[char] += 1
        else:
            counter[char] = 1

    has_two, has_three = False, False
    for k, v in counter.items():
        if v == 2:
            has_two = True
        elif v == 3:
            has_three = True

    return has_two, has_three


def count_diff(box1, box2):
    count_diff = 0
    samesies = list()
    for char1, char2 in zip(box1, box2):
        if char1 != char2:
            count_diff += 1
        else:
            samesies.append(char1)

        if count_diff > 1:
            return
    if count_diff == 1:
        return ''.join(samesies)


def find_diff(list_of_boxes):
    for i, box1 in enumerate(list_of_boxes):
        for box2 in list_of_boxes[i + 1:]:
            repeat_flag = count_diff(box1, box2)

            if repeat_flag:
                return repeat_flag


TEST_BOXES = [
    "abcdef",
    "bababc",
    "abbcde",
    "abcccd",
    "aabcdd",
    "abcdee",
    "ababab",
]

TEST_BOXES_SIMILAR = [
    'abcde',
    'fghij',
    'klmno',
    'pqrst',
    'fguij',
    'axcye',
    'wvxyz',
]

assert check_for_repeats(TEST_BOXES[0]) == (False, False)
assert check_for_repeats(TEST_BOXES[1]) == (True, True)
assert check_for_repeats(TEST_BOXES[2]) == (True, False)
assert check_for_repeats(TEST_BOXES[3]) == (False, True)
assert check_for_repeats(TEST_BOXES[4]) == (True, False)
assert check_for_repeats(TEST_BOXES[5]) == (True, False)
assert check_for_repeats(TEST_BOXES[6]) == (False, True)

assert create_checksum(TEST_BOXES) == 12

assert count_diff('abcde', 'fghij') is None
assert count_diff('fghij', 'fguij') == 'fgij'

if __name__ == '__main__':
    list_of_boxes = create_list_of_boxes()
    print(create_checksum(list_of_boxes))
    print(find_diff(list_of_boxes))

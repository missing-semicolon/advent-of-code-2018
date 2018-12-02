"""
https://adventofcode.com/2018/day/1
"""


def parse_input():
    in_list = list()
    with open('./day1_input.txt', 'r') as f:
        for line in f:
            in_list.append(int(line))

    return in_list


def apply_changes(change_list):
    frequency = 0
    for change in change_list:
        frequency += change
    return frequency


def apply_change_with_stop_repeat(change_list):
    freq_set = set()
    frequency = 0

    index = 0
    while frequency not in freq_set:
        freq_set.add(frequency)
        change = change_list[index]
        frequency += change
        index += 1
        index = index % len(change_list)
    return frequency


assert apply_changes([1, 1, 1]) == 3
assert apply_changes([1, 1, -2]) == 0
assert apply_changes([-1, -2, -3]) == -6

assert apply_change_with_stop_repeat([1, -2, 3, 1]) == 2
assert apply_change_with_stop_repeat([1, -1]) == 0
assert apply_change_with_stop_repeat([-6, 3, 8, 5, -6]) == 5
assert apply_change_with_stop_repeat([7, 7, -2, -7, -4]) == 14

if __name__ == '__main__':
    in_list = parse_input()

    in_list = parse_input()
    answer1 = apply_changes(in_list)
    print(answer1)

    print(apply_change_with_stop_repeat(in_list))

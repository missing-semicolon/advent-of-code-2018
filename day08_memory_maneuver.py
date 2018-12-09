from typing import List, NamedTuple

TEST_STRING = "2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2"


class Node(NamedTuple):
    child_ct: int
    metadata_ct: int
    metadata: List[int]

    def metadata_sum(self):
        return sum(self.metadata)


test_list = TEST_STRING.split()


def parse_node(input_list: List[int], node_ct: int) -> List[Node]:
    child_ct = input_list[0]
    metadata_ct = input_list[1]
    if node_ct == 1 and child_ct == 0:
        metadata = input_list[2:2 + metadata_ct]
        return [Node(child_ct, metadata_ct, metadata)]
    elif node_ct > 1 and child_ct == 0:
        metadata = input_list[2:2 + metadata_ct]
        return [Node(child_ct, metadata_ct, metadata)] + parse_node(input_list[2 + metadata_ct:], node_ct - 1)
    elif child_ct > 0:
        children = parse_node(input_list[2:], child_ct)
        digits_to_skip = sum([2 + child.metadata_ct for child in children]) + 2
        metadata = input_list[digits_to_skip:digits_to_skip + metadata_ct]
        return [Node(child_ct, metadata_ct, metadata)] + children


def parse_full_list(input_list: List[int]) -> List[Node]:
    child_ct = input_list[0]
    metadata_ct = input_list[1]
    children = parse_node(input_list[2:], child_ct)
    digits_to_skip = sum([2 + child.metadata_ct for child in children]) + 2
    metadata = input_list[digits_to_skip:digits_to_skip + metadata_ct]
    if digits_to_skip + metadata_ct < len(input_list):
        remainder = parse_full_list(input_list[digits_to_skip + metadata_ct:])
        return [Node(child_ct, metadata_ct, metadata)] + children + remainder
    else:
        output = [Node(child_ct, metadata_ct, metadata)] + children
        print(sum([2 + child.metadata_ct for child in output]))
        return output


assert parse_node([0, 1, 99], 1) == [Node(0, 1, [99])]
assert parse_node([0, 3, 10, 11, 12, 0, 1, 2], 2) == [
    Node(0, 3, [10, 11, 12]), Node(0, 1, [2])
]

assert parse_node([1, 1, 0, 1, 99, 2], 1) == [
    Node(1, 1, [2]), Node(0, 1, [99])
]

assert parse_node([0, 3, 10, 11, 12, 1, 1, 0, 1, 99, 2], 2) == [
    Node(0, 3, [10, 11, 12]),
    Node(1, 1, [2]),
    Node(0, 1, [99]),
]

assert parse_full_list([int(x) for x in TEST_STRING.split()]) == [
    Node(2, 3, [1, 1, 2]),
    Node(0, 3, [10, 11, 12]),
    Node(1, 1, [2]),
    Node(0, 1, [99]),
]

assert sum([node.metadata_sum() for node in parse_full_list([int(x) for x in TEST_STRING.split()])]) == 138

def load_data():
    with open('./data/day08_input.txt', 'r') as f:
        return [int(x) for x in f.read().split()]


input_data = load_data()
parsed_nodes = parse_full_list(input_data)
print(sum([node.metadata_sum() for node in parsed_nodes]))

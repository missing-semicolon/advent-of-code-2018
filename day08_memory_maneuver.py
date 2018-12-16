from typing import List, NamedTuple

TEST_STRING = "2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2"
TEST = [int(x) for x in TEST_STRING.split()]


class Node(NamedTuple):
    child_ct: int
    metadata_ct: int
    children: List['Node']
    metadata: List[int]

    def metadata_sum(self):
        return sum(self.metadata)


test_list = TEST_STRING.split()


def parse_node(input_list: List[int], start: int = 0) -> List[Node]:
    child_ct = input_list[start]
    metadata_ct = input_list[start + 1]
    children = []
    start = start + 2

    for _ in range(child_ct):
        child, start = parse_node(input_list, start)
        children.append(child)

    metadata = input_list[start:start + metadata_ct]
    return Node(child_ct, metadata_ct, children, metadata), (start + metadata_ct)


assert parse_node([0, 1, 99], 0) == (Node(0, 1, [], [99]), 3)
assert parse_node([1, 1, 0, 1, 99, 2], 0) == (
    Node(1, 1, [Node(0, 1, [], [99])], [2]), 6
)

def sum_metadata(node: Node):
    return sum(node.metadata) + sum([sum_metadata(child) for child in node.children])

TEST_NODE, _ = parse_node(TEST)
assert sum_metadata(TEST_NODE) == 138


with open('./data/day08_input.txt', 'r') as f:
    raw = f.read().strip()
input_data = [int(x) for x in raw.split()]
print('Input length', len(input_data))
node, _ = parse_node(input_data)
print(sum_metadata(node))


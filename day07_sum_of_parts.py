from typing import List, Dict
import re

rgx = 'Step ([A-Z]) must be finished before step ([A-Z]) can begin'

TEST_DIRECTIONS = """Step C must be finished before step A can begin.
Step C must be finished before step F can begin.
Step A must be finished before step B can begin.
Step A must be finished before step D can begin.
Step B must be finished before step E can begin.
Step D must be finished before step E can begin.
Step F must be finished before step E can begin.
"""


def load_data() -> str:
    with open('./data/day07_input.txt', 'r') as f:
        return [line.strip() for line in f.readlines()]


def create_direction_dict(direction_list: List[str]) -> Dict[str, List[str]]:
    parent_to_child = dict()
    child_to_parents = dict()
    rgx_out = [re.match(rgx, direction).groups()
               for direction in direction_list]

    for [parent, child] in rgx_out:
        if parent in parent_to_child.keys():
            parent_to_child[parent].append(child)
            parent_to_child[parent] = sorted(parent_to_child[parent])
        else:
            parent_to_child[parent] = [child]

        if child in child_to_parents.keys():
            child_to_parents[child].append(parent)
        else:
            child_to_parents[child] = [parent]
    return parent_to_child, child_to_parents


def add_children_to_pending(parent, pending, parent_to_child):
    for child in parent_to_child[parent]:
        if child not in pending:
            pending.append(child)
    return pending


def create_order(parent_to_child: Dict[str, List[str]],
                 child_to_parents: Dict[str, List[str]]) -> List[str]:
    # Find the head:
    parents = set()
    children = set()
    for parent, child_list in parent_to_child.items():
        parents.add(parent)
        for child in child_list:
            children.add(child)

    head = parents - children
    if len(head) > 1:
        for head_cand in head:
            if head_cand in parent_to_child.keys():
                head = head_cand
                break
    else:
        head = head.pop()

    order = list()
    done = set()
    pending = list()

    order.append(head)
    done.add(head)
    pending = add_children_to_pending(head, pending, parent_to_child)
    while len(pending) > 0:
        for candidate in sorted(pending):
            if all(cand_parent in done for cand_parent in child_to_parents[candidate]):  # noqa: E501
                order.append(candidate)
                done.add(candidate)
                pending.remove(candidate)
                if candidate in parent_to_child.keys():
                    pending = add_children_to_pending(
                        candidate, pending, parent_to_child)
                break
    return ''.join(order)


parent_to_child, child_to_parents = create_direction_dict(
    [line for line in TEST_DIRECTIONS.strip().split('\n')]
)

assert create_order(parent_to_child, child_to_parents) == 'CABDFE'

directions = load_data()
parent_to_child, child_to_parents = create_direction_dict(directions)
print(create_order(parent_to_child, child_to_parents))

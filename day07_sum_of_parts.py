from typing import List, Dict, Set, Tuple
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

RelationDict = Dict[str, List[str]]


def load_data() -> List[str]:
    with open('./data/day07_input.txt', 'r') as f:
        return [line.strip() for line in f.readlines()]


def create_direction_dict(
    direction_list: List[str]
) -> Tuple[RelationDict, RelationDict]:

    parent_to_child: Dict = dict()
    child_to_parents: Dict = dict()
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


def add_children_to_pending(parent: str,
                            pending: List[str],
                            parent_to_child: RelationDict):
    for child in parent_to_child[parent]:
        if child not in pending:
            pending.append(child)
    return pending


def create_order(parent_to_child: Dict[str, List[str]],
                 child_to_parents: Dict[str, List[str]]) -> str:
    # Find the head:
    parents = set()
    children = set()
    for parent, child_list in parent_to_child.items():
        parents.add(parent)
        for child in child_list:
            children.add(child)

    head = parents - children
    pending = list(head)

    order: List = list()
    done: Set = set()

    while len(pending) > 0:
        for candidate in sorted(pending):
            if (
                    candidate in child_to_parents.keys()
                    and all(cand_parent in done
                            for cand_parent in child_to_parents.get(candidate))
                ) or (
                    candidate not in child_to_parents.keys()
            ):
                order.append(candidate)
                done.add(candidate)
                pending.remove(candidate)
                if candidate in parent_to_child.keys():
                    pending = add_children_to_pending(
                        candidate, pending, parent_to_child)
                break
    return ''.join(order)


def ready_to_work(candidate, child_to_parents, done):
    return (
        candidate in child_to_parents.keys() and
        all(cand_parent in done for cand_parent in child_to_parents.get(candidate))  # noqa: E501
    ) or (
        candidate not in child_to_parents.keys()
    )


def create_order_with_helpers(parent_to_child: Dict[str, List[str]],
                              child_to_parents: Dict[str, List[str]],
                              helpers: int,
                              base_time: int = 0) -> int:
    # Find the head:
    parents = set()
    children = set()
    for parent, child_list in parent_to_child.items():
        parents.add(parent)
        for child in child_list:
            children.add(child)

    head = parents - children
    pending = {k: ord(k) - 64 + base_time for k in head}

    order: List = list()
    done: Set = set()
    working: Set = set()

    counter = 0
    while len(pending.keys()) > 0:
        for candidate in sorted(list(pending)):
            if ready_to_work(candidate, child_to_parents, done):
                working.add(candidate)
            if len(working) > helpers:
                break

        for task in working:
            pending[task] -= 1
            if pending[task] == 0:
                del pending[task]
                done.add(task)
                order.append(task)
                if task in parent_to_child.keys():
                    for child in parent_to_child[task]:
                        pending[child] = ord(child) - 64 + base_time
        for completed in done:
            if completed in working:
                working.remove(completed)
        counter += 1
    return counter


parent_to_child, child_to_parents = create_direction_dict(
    [line for line in TEST_DIRECTIONS.strip().split('\n')]
)

assert create_order(parent_to_child, child_to_parents) == 'CABDFE'
assert create_order_with_helpers(parent_to_child, child_to_parents, 1) == 15

directions = load_data()
parent_to_child, child_to_parents = create_direction_dict(directions)
print(create_order(parent_to_child, child_to_parents))
print(create_order_with_helpers(parent_to_child, child_to_parents, 4, 60))

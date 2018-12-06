from typing import Set
import re

def load_data() -> str:
    with open('./data/day05_input.txt', 'r') as f:
        data = [line.strip() for line in f.readlines()]

    return ''.join(data)


def replace_rule(a: str, b: str) -> bool:
    return a != b and a.upper() == b.upper()


def replace_matches(x: str) -> str:
    replaced = True
    while replaced:
        replaced = False
        for i in range(1, len(x)):
            prev = x[i - 1]
            cur = x[i]
            if replace_rule(prev, cur):
                x = x[:i - 1] + x[i + 1:]
                replaced = True
                break
    return x


def get_unit_types(polymer: str) -> Set[str]:
    return {char for char in polymer.lower()}


def remove_type(polymer: str, type: str) -> str:
    return re.sub(type, '', polymer, flags=re.IGNORECASE)


def improve_polymer(polymer: str) -> int:
    polymer_lengths = list()
    unit_types = get_unit_types(polymer)

    for unit_type in unit_types:
        shortened = remove_type(polymer, unit_type)
        polymer_lengths.append(len(replace_matches(shortened)))

    return sorted(polymer_lengths)[0]


assert replace_rule('a', 'A') is True
assert replace_rule('a', 'a') is False
assert replace_rule('a', 'b') is False
assert replace_matches('aA') == ''
assert replace_matches('aAc') == 'c'
assert replace_matches('abBA') == ''
assert replace_matches('abAB') == 'abAB'
assert replace_matches('aabAAB') == 'aabAAB'
assert replace_matches('dabAcCaCBAcCcaDA') == 'dabCBAcaDA'

assert remove_type('dabAcCaCBAcCcaDA', 'a') == 'dbcCCBcCcD'
assert improve_polymer('dabAcCaCBAcCcaDA') == 4

data = load_data()
# print(len(replace_matches(data)))
print(improve_polymer(data))


def load_data() -> str:
    with open('./data/day05_input.txt', 'r') as f:
        data = [line.strip() for line in f.readlines()]

    return ''.join(data)

def replace_matches(x: str) -> str:
    if len(x) == 1:
        return x

    for i, (cur, nxt) in enumerate(zip(x[:-1], x[1:])):
        if i == len(x):
            return x
        if cur != nxt and (cur == nxt.upper() or cur.upper() == nxt):
            if len(x) == 2:
                return ''
            else:
                x = x[:i] + x[i + 2:]
                x = replace_matches(x)
                return x
    return x


assert replace_matches('aAc') == 'c'
assert replace_matches('aA') == ''
assert replace_matches('abBA') == ''
assert replace_matches('abAB') == 'abAB'
assert replace_matches('aabAAB') == 'aabAAB'
assert replace_matches('dabAcCaCBAcCcaDA') == 'dabCBAcaDA'

data = load_data()
print(replace_matches(data))
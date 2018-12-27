from typing import Tuple, List

SERIAL_NUMBER = 1308


def get_hundreds(x: int) -> int:
    if x < 100:
        return 0
    else:
        return (x % 1000 - x % 100) // 100


def get_power_from_coord(coord: Tuple[int, int], serial_number=SERIAL_NUMBER) -> int:
    x, y = coord
    rack_id = x + 10
    power_level = rack_id * y
    power_level += serial_number
    power_level = power_level * rack_id
    power_level = get_hundreds(power_level)
    power_level -= 5

    return power_level


assert get_power_from_coord((3, 5), serial_number=8) == 4

assert get_power_from_coord((122, 79), 57) == -5
assert get_power_from_coord((217, 196), 39) == 0
assert get_power_from_coord((101, 153), 71) == 4

grid = [[get_power_from_coord((x, y)) for x in range(300)] for y in range(300)]


def get_grid_power(coord: Tuple[int, int], grid: List[List[int]], size: int = 3) -> int:
    power = 0
    x, y = coord
    for x_slice in range(size):
        for y_slice in range(size):
            if (y + y_slice) >= 300 or (x + x_slice) >= 300:
                cell_power = 0
            else:
                cell_power = grid[y + y_slice][x + x_slice]
            # print(cell_power)
            power += cell_power
    return power


def create_power_grid(serial_number):
    return [[get_power_from_coord((x, y), serial_number) for x in range(300)] for y in range(300)]


assert get_grid_power((33, 45), create_power_grid(18)) == 29
assert get_grid_power((21, 61), create_power_grid(42)) == 30


def find_max_coord(grid: List[List[int]]) -> Tuple[int, int]:
    power = -1e20
    out_tuple = None
    for x in range(300):
        for y in range(300):
            proposal = get_grid_power((x, y), grid)
            if proposal > power:
                power = proposal
                out_tuple = (x, y)
    return out_tuple


def find_max_coord_any_size(grid: List[List[int]]) -> Tuple[int, int]:
    power = -1e20
    out_tuple = None
    results = {}
    for x in range(300):
        for y in range(300):
            results[(x, y, 1)] = get_grid_power((x, y), grid, 1)

    for x in range(300):
        for y in range(300):
            print(x, y)
            for size in range(2, min(300 - x, 300 - y)):
                results[(x, y, size)] = results[(x, y, size - 1)]
                for i in range(size):
                    results[(x, y, size)] += grid[y + size][x + i]
                    results[(x, y, size)] += grid[y + i][x + size]
                results[(x, y, size)] += grid[y + size][x + size]

    for k, v in results.items():
        if v > power:
            power = v
            out_tuple = k
    return out_tuple


assert find_max_coord(create_power_grid(18)) == (33, 45)
assert find_max_coord(create_power_grid(42)) == (21, 61)

print(find_max_coord(create_power_grid(SERIAL_NUMBER)))
# print(find_max_coord_any_size(create_power_grid(SERIAL_NUMBER)))
print(find_max_coord_any_size(create_power_grid(18)))

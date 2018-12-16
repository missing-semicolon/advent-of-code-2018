from typing import List

"""
0, (1), 2

1 + 1 % 3 = 2
1 + 2 % 3 = 0

0, 1, (2), 3

2 + 1 % 4 = 3
2 + 2 % 4 = 0

0, 1, 2, (3)

3 + 1 % 4 = 0
3 + 2 % 4 = 1
"""

def play_game(num_players: int, highest_marble: int) -> int:
    circle = [0]
    current_marble = 0

    for marble in range(highest_marble + 1):
        if marble == 0:
            continue

        player = marble % num_players
        if marble % 23 != 0:
            if len(circle) == 1:
                circle = circle + [marble]
                current_marble = 1
                print(player, circle)
                continue
            break_point_left = (current_marble + 1) % len(circle)
            if break_point_left == len(circle) - 1:
                circle = circle[:break_point_left + 1] + [marble]
                current_marble = break_point_left + 1
            else:
                break_point_right = (current_marble + 2) % len(circle)
                circle = circle[:break_point_left + 1] + [marble] + circle[(break_point_right):]
                current_marble = break_point_right
            print(player, circle, circle[current_marble])

play_game(9, 22)
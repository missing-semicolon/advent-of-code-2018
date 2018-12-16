from typing import List, Dict

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


def play_game_old(num_players: int, highest_marble: int) -> int:
    circle: List[int] = [0]
    current_marble: int = 0
    scoreboard: Dict[int, int] = {x: 0 for x in range(num_players + 1)}

    for marble in range(highest_marble + 1):
        if marble == 0:
            continue

        player = marble % num_players
        if player == 0:
            player = num_players
        if marble % 23 != 0:
            if len(circle) == 1:
                circle = circle + [marble]
                current_marble = 1
                continue
            break_point_left = (current_marble + 1) % len(circle)
            if break_point_left == len(circle) - 1:
                circle = circle[:break_point_left + 1] + [marble]
                current_marble = break_point_left + 1
            else:
                break_point_right = (current_marble + 2) % len(circle)
                circle = circle[:break_point_left + 1] + \
                    [marble] + circle[(break_point_right):]
                current_marble = break_point_right
        else:
            scoreboard[player] += marble
            take_index = (current_marble - 7) % len(circle)
            take_marble = circle[take_index]
            scoreboard[player] += take_marble
            circle.remove(take_marble)
            current_marble = take_index
    return max([v for v in scoreboard.values()])


# assert play_game(9, 25) == 32
# assert play_game(10, 1618) == 8317
# assert play_game(13, 7999) == 146373
# assert play_game(17, 1104) == 2764
# assert play_game(21, 6111) == 54718
# assert play_game(30, 5807) == 37305

# 459 players; last marble is worth 72103 points
print(play_game_old(459, 72103))

# print(play_game(459, (459 * 23 * 1) + 21))
# print(play_game(459, (459 * 23 * 2) + 21))

# print(play_game(459, 72103 * 100))

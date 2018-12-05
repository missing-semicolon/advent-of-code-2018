from typing import List, Tuple, Dict
from collections import Counter
from datetime import datetime
import re


LogEntry = Tuple[datetime, str]


def load_data() -> List[str]:
    with open('./data/day04_input.txt', 'r') as f:
        raw_record = [line.strip().lower() for line in f.readlines()]

    return raw_record


def parse_line(line: str) -> LogEntry:
    rgx = "\[(\d{4}-\d{2}-\d{2} \d{2}:\d{2})\] (.*)"
    matches = re.match(rgx, line.lower())
    if matches is None:
        raise Exception()
    parse_date, message = matches.groups()
    return datetime.strptime(parse_date, '%Y-%m-%d %H:%M'), message


TEST_LOG = [
    '[1518-11-01 00:00] Guard #10 begins shift',
    '[1518-11-01 00:05] falls asleep',
    '[1518-11-01 00:25] wakes up',
    '[1518-11-01 00:30] falls asleep',
    '[1518-11-01 00:55] wakes up',
    '[1518-11-01 23:58] Guard #99 begins shift',
    '[1518-11-02 00:40] falls asleep',
    '[1518-11-02 00:50] wakes up',
    '[1518-11-03 00:05] Guard #10 begins shift',
    '[1518-11-03 00:24] falls asleep',
    '[1518-11-03 00:29] wakes up',
    '[1518-11-04 00:02] Guard #99 begins shift',
    '[1518-11-04 00:36] falls asleep',
    '[1518-11-04 00:46] wakes up',
    '[1518-11-05 00:03] Guard #99 begins shift',
    '[1518-11-05 00:45] falls asleep',
    '[1518-11-05 00:55] wakes up',
]


def create_log(sorted_data: List[LogEntry]) -> Dict[int, Counter]:
    sleep_log: Dict = dict()
    for curr, fut in zip(sorted_data, sorted_data[1:]):
        curr_time, curr_message = curr
        fut_time, fut_message = fut

        if re.search('#\d+', curr_message):  # Start of log
            matches = re.search('#(\d+)', curr_message)
            if matches is None:
                raise Exception()
            guard = int(matches.groups()[0])
        elif 'falls asleep' in curr_message and 'wakes up' in fut_message:  # Sleep Period
            sleep_minutes = [m for m in range(
                curr_time.minute, fut_time.minute)]

            if guard in sleep_log:
                sleep_log[guard] += Counter(sleep_minutes)
            else:
                sleep_log[guard] = Counter(sleep_minutes)

    return sleep_log


def strategy_one(sleep_log: Dict[int, Counter]) -> int:
    max_sleep_guard = 0
    max_sleep_minute = 0
    max_sleep_time = -1e10
    for k, v in sleep_log.items():
        if sum(v.values()) > max_sleep_time:
            max_sleep_guard = k
            max_sleep_minute = v.most_common(1)[0][0]
            max_sleep_time = sum(v.values())
    return max_sleep_guard * max_sleep_minute


def strategy_two(sleep_log: Dict[int, Counter]) -> int:
    most_frequent = 0
    frequent_minute = 0
    frequent_guard = 0
    for guard, v in sleep_log.items():
        minute, frequent = v.most_common(1)[0]
        if frequent > most_frequent:
            most_frequent = frequent
            frequent_minute = minute
            frequent_guard = guard

    return frequent_guard * frequent_minute


assert parse_line(TEST_LOG[0]) == (
    datetime(1518, 11, 1, 0, 0), 'guard #10 begins shift')

assert strategy_one(create_log(
    sorted([parse_line(x) for x in TEST_LOG]))) == 240

assert strategy_two(create_log(
    sorted([parse_line(x) for x in TEST_LOG]))) == 4455

raw = load_data()
parsed = sorted([parse_line(line) for line in raw])
print(strategy_one(create_log(parsed)))

print(strategy_two(create_log(parsed)))

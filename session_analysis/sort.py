import json
import sys

def get_duration(json_str):
    data = json.loads(json_str)
    return data.get('total_duration', 0)

lines = sys.stdin.readlines()

# 각 줄을 total_duration 값에 따라 정렬
lines.sort(key=lambda line: get_duration(line.split('\t', 1)[1]), reverse=True)

for line in lines:
    print(line, end='')


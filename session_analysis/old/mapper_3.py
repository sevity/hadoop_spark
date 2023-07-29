#!/usr/bin/env python3

import sys
import json
from datetime import datetime
import logging

logging.basicConfig(stream=sys.stderr, level=logging.ERROR)

previous_session_id = None
url_list = []
start_time = None
end_time = None

def reset_variables():
    global url_list, start_time, end_time
    url_list = []
    start_time = None
    end_time = None

for line in sys.stdin:
    try:
        parts = line.strip().split()
        if len(parts) != 15:
            continue

        date_time = parts[0] + " " + parts[1]
        date_time = datetime.strptime(date_time, '%Y-%m-%d %H:%M:%S')

        session_id = parts[2]
        url = parts[4]

        if previous_session_id and previous_session_id != session_id:
            print('%s\t%s' % (previous_session_id, json.dumps({"start_time": str(start_time), "end_time": str(end_time), "duration": (end_time - start_time).total_seconds(), "url_list": list(set(url_list))})))
            reset_variables()

        if not start_time or date_time < start_time:
            start_time = date_time
        if not end_time or date_time > end_time:
            end_time = date_time

        url_list.append(url)
        previous_session_id = session_id

    except Exception as e:
        logging.error(f"Error processing line: {line.strip()}, Error: {e}")

# 마지막 세션 출력
if previous_session_id:
    print('%s\t%s' % (previous_session_id, json.dumps({"start_time": str(start_time), "end_time": str(end_time), "duration": (end_time - start_time).total_seconds(), "url_list": list(set(url_list))})))


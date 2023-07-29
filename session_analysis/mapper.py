#!/usr/bin/env python3

import sys
import json
import codecs
from datetime import datetime, timedelta
import logging

logging.basicConfig(stream=sys.stderr, level=logging.ERROR)

previous_ip = None
url_list = []
start_time = None
end_time = None
session_timeout = timedelta(seconds=1800)  # 1800 seconds = 30 minutes

def reset_variables():
    global url_list, start_time, end_time
    url_list = []
    start_time = None
    end_time = None

# Using codecs to get stdin with a fallback in case of a UTF-8 decoding error
stdin = codecs.getreader('utf-8')(sys.stdin.buffer, errors='ignore')

for line in stdin:
    try:
        parts = line.strip().split()
        if len(parts) != 15:
            continue

        date_time = parts[0] + " " + parts[1]
        date_time = datetime.strptime(date_time, '%Y-%m-%d %H:%M:%S')

        ip = parts[8]  # changed from parts[2] to parts[8] to use the client IP
        url = parts[4]

        # If there is a previous ip and the current ip is different or a session timeout has occurred
        if previous_ip and (previous_ip != ip or (date_time - end_time) > session_timeout):
            print('%s\t%s' % (previous_ip, json.dumps({"start_time": str(start_time), "end_time": str(end_time), "duration": (end_time - start_time).total_seconds(), "url_list": list(set(url_list))})))
            reset_variables()

        if not start_time or date_time < start_time:
            start_time = date_time
        if not end_time or date_time > end_time:
            end_time = date_time

        url_list.append(url)
        previous_ip = ip

    except Exception as e:
        logging.error(f"Error processing line: {line.strip()}, Error: {e}")

# Print the last session
if previous_ip:
    print('%s\t%s' % (previous_ip, json.dumps({"start_time": str(start_time), "end_time": str(end_time), "duration": (end_time - start_time).total_seconds(), "url_list": list(set(url_list))})))


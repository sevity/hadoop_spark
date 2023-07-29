#!/usr/bin/env python3

import sys
import json

previous_ip = None
total_duration = 0.0
url_list = []
start_time = None
end_time = None

for line in sys.stdin:
    ip, session_info = line.strip().split('\t')
    session_info = json.loads(session_info)

    if previous_ip and previous_ip != ip:
        print('%s\t%s' % (previous_ip, json.dumps({"total_duration": total_duration, "url_list": list(set(url_list)), "start_time": start_time, "end_time": end_time})))

        total_duration = 0.0
        url_list = []
        start_time = None
        end_time = None

    if not start_time or session_info["start_time"] < start_time:
        start_time = session_info["start_time"]
    if not end_time or session_info["end_time"] > end_time:
        end_time = session_info["end_time"]

    total_duration += float(session_info["duration"])
    url_list.extend(session_info["url_list"])

    previous_ip = ip

if previous_ip:
    print('%s\t%s' % (previous_ip, json.dumps({"total_duration": total_duration, "url_list": list(set(url_list)), "start_time": start_time, "end_time": end_time})))


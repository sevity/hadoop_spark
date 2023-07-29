#!/usr/bin/env python3
import sys
import json
import logging
from datetime import datetime, timedelta

session_id = None
session_data = []

# 로그를 파싱하는 함수
def parse_log_line(line):
    if line.startswith("#") or not line.strip():
        return None

    parts = line.split(" ")
    if len(parts) < 5:
        return None

    data = {
        "timestamp": parts[0] + " " + parts[1],
        "ip": parts[2],
        "url": parts[4]
    }
    return data

# 세션을 처리하는 함수
def handle_session(session_id, session_data):
    if session_id is not None and len(session_data) > 0:
        session_start = datetime.strptime(session_data[0]['timestamp'], "%Y-%m-%d %H:%M:%S")
        session_end = datetime.strptime(session_data[-1]['timestamp'], "%Y-%m-%d %H:%M:%S")
        session_duration = (session_end - session_start).total_seconds()
        
        print(f"Session ID: {session_id}, Start: {session_start}, End: {session_end}, Duration: {session_duration} seconds, URLs: {[data['url'] for data in session_data]}")

# 세션 타임아웃 설정 (예: 30분)
SESSION_TIMEOUT = timedelta(minutes=30)

for raw_line in sys.stdin:
    try:
        line = raw_line.strip()
        data = parse_log_line(line)

        if data is None:
            continue

        if session_id is None:
            session_id = data['ip']
            session_data.append(data)
        else:
            current_timestamp = datetime.strptime(data['timestamp'], "%Y-%m-%d %H:%M:%S")
            previous_timestamp = datetime.strptime(session_data[-1]['timestamp'], "%Y-%m-%d %H:%M:%S")

            # IP가 변경되거나, 세션 타임아웃이 발생하면 이전 세션을 종료하고 새 세션을 시작
            if data['ip'] != session_id or (current_timestamp - previous_timestamp) > SESSION_TIMEOUT:
                handle_session(session_id, session_data)
                session_id = data['ip']
                session_data = [data]
            else:
                session_data.append(data)

    except Exception as e:
        logging.error(f"Error processing line: {raw_line}, Error: {e}")
        continue

# 마지막 세션을 처리
handle_session(session_id, session_data)


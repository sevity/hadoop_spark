from collections import Counter
import json

def get_most_active_hours(filename):
    with open(filename, 'r') as f:
        data = f.readlines()
    ip_to_hour = {}
    for line in data:
        ip, json_str = line.strip().split('\t')
        session_info = json.loads(json_str)
        start_time_str = session_info['start_time']
        end_time_str = session_info['end_time']
        start_hour = int(start_time_str.split(" ")[1].split(":")[0])
        end_hour = int(end_time_str.split(" ")[1].split(":")[0])
        hours = list(range(start_hour, end_hour+1))
        if ip in ip_to_hour:
            ip_to_hour[ip].extend(hours)
        else:
            ip_to_hour[ip] = hours
    ip_to_most_active_hour = {}
    for ip, hours in ip_to_hour.items():
        most_active_hour = Counter(hours).most_common(1)[0][0]
        ip_to_most_active_hour[ip] = most_active_hour
    return ip_to_most_active_hour

def print_most_active_hours(filename):
    ip_to_most_active_hour = get_most_active_hours(filename)
    for ip, hour in ip_to_most_active_hour.items():
        print(f"IP Address: {ip} - Most active hour: {hour}")

print_most_active_hours("mapper_output.txt")


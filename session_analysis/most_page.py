import json
from collections import Counter

def get_most_common_urls(filename):
    with open(filename, 'r') as f:
        data = f.readlines()
    ip_to_url = {}
    for line in data:
        ip, json_str = line.strip().split('\t')
        url_list = json.loads(json_str)['url_list']
        most_common_url = Counter(url_list).most_common(1)[0][0]
        ip_to_url[ip] = most_common_url
    return ip_to_url

def print_most_common_urls(filename):
    ip_to_url = get_most_common_urls(filename)
    for ip, url in ip_to_url.items():
        print(f"IP Address: {ip} - Most visited page: {url}")

print_most_common_urls("reducer_output.txt")


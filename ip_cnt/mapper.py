import sys
import logging

# Set up logging
# logging.basicConfig(filename="mapper.log", level=logging.DEBUG)
logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

# Ignore bad characters
for line in sys.stdin.buffer:
    try:
        line = line.decode('utf-8', 'ignore')
    except UnicodeDecodeError as e:
        logging.error(f"Error decoding line: {line.strip()}, Error: {e}")
        continue

    try:
        data = line.strip().split(" ")
        if len(data) == 15:
            date, time, s_ip, cs_method, cs_uri_stem, cs_uri_query, s_port, cs_username, c_ip, cs_user_agent, cs_referer, sc_status, sc_substatus, sc_win32_status, time_taken = data
            logging.debug(f"Client IP: {c_ip}, Count: 1")
            print("{0}\t{1}".format(c_ip, 1))
    except Exception as e:
        # 예외 발생 시 로그 기록
        logging.error(f"Error processing line: {line.strip()}, Error: {e}")

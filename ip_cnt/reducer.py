#!/usr/bin/env python3

import sys
import logging

# Set up logging
logging.basicConfig(filename="reducer.log", level=logging.DEBUG)

last_key = None
running_total = 0
key = None

try:
    for input in sys.stdin:
        key, value = input.strip().split("\t", 1)
        if last_key == key:
            running_total += int(value)
        else:
            if last_key:
                logging.debug(f"Key: {last_key}, Running Total: {running_total}")
                print("{0}\t{1}".format(last_key, running_total))
            running_total = int(value)
            last_key = key

    if last_key == key and key is not None:
        logging.debug(f"Key: {last_key}, Running Total: {running_total}")
        print("{0}\t{1}".format(last_key, running_total))

except Exception as e:
    # 예외 발생 시 로그 기록
    logging.error(f"Error processing input: {e}")


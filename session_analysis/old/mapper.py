#!/usr/bin/env python3
import sys
import logging

logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

for line in sys.stdin:
    line = line.strip()
    
    try:
        if not line.startswith('#'):  # skip lines starting with '#'
            elements = line.split(' ')
            date_time = elements[0] + ' ' + elements[1]
            ip = elements[8]
            url = elements[4]
            print('%s\t%s\t%s' % (date_time, ip, url))
    except Exception as e:
        logging.error(f"Error processing line: {line.strip()}, Error: {e}")


from pyspark import SparkConf, SparkContext
from datetime import datetime, timedelta
from pyspark.sql import SparkSession

def parse_log_line(line):
    try:
        parts = line.strip().split()
        if len(parts) != 15:
            return None

        date_time = parts[0] + " " + parts[1]
        date_time = datetime.strptime(date_time, '%Y-%m-%d %H:%M:%S')
        url = parts[4]
        ip = parts[8]  # changed from parts[2] to parts[8] to use the client IP

        return (ip, (date_time, url))
    except:
        return None


def calculate_sessions(group):
    ip, data = group
    data = list(data)
    data.sort(key = lambda x: x[0])
    sessions = []
    session = [data[0]]
    for i in range(1, len(data)):
        if datetime.strptime(data[i][0], '%Y-%m-%d %H:%M:%S') - datetime.strptime(session[-1][0], '%Y-%m-%d %H:%M:%S') > timedelta(seconds=1800):
            sessions.append((ip, session))
            session = [data[i]]
        else:
            session.append(data[i])
    sessions.append((ip, session))
    return sessions

# Spark configuration
conf = SparkConf().setMaster('local').setAppName('Log Analysis')
sc = SparkContext(conf=conf)

log_lines = sc.textFile('hdfs://localhost:9000/logs/u_ex230501*')
parsed_lines = log_lines.map(parse_log_line).filter(lambda x: x is not None)
parsed_sample = parsed_lines.take(10)  # take the first 10 records
print("size of parsed_sample: "+str(len(parsed_sample)))
for record in parsed_sample:
    print("---sevity--- "+str(record))
grouped_by_ip = parsed_lines.groupByKey()
sessions = grouped_by_ip.flatMap(calculate_sessions)
sessions.saveAsTextFile('hdfs://localhost:9000/session_output')


#!/usr/bin/python
import sys
import json
import subprocess
from threading import Thread


# Group
group = "Service availability"

# Description of metrics
description = "Check remote service availability"

# Hosts to check
hosts = {
    # "{{Service availability name of the host}}": { "host": "{{hostname/ip address}}", "port": {{port}} },
    # ex "Service availability google dns": { "host": "8.8.8.8", "port": 53 },
    "Service availability google dns": { "host": "8.8.8.8", "port": 53 },
    "Service availability coscale api": { "host": "37.187.86.75", "port": 80 },
    "Service availability coscale dns": { "host": "37.187.86.75", "port": 53 }, # No service is running here
}

#
# DONT CHANGE ANYTHING BELOW THIS LINE
#

def execute(metricId, host, port):
    pingtime = subprocess.check_output("nc -w 1 %s %s && echo $? || echo $?" % (host, port), shell=True)
    sys.stdout.write("M%s %s\n" % (metricId, pingtime.rstrip()))

def config():
    metrics = []
    counter = 0;
    for host in hosts:
        metrics.append({
            "id": counter,
            "datatype": "DOUBLE",
            "name": host,
            "description": description,
            "groups": group,
            "unit": "",
            "tags": "",
            "calctype": "Instant"
        })
        counter += 1

    print json.dumps({
        "maxruntime": 5000,
        "metrics": metrics
    })

def data():
    datapoints = {}
    counter = 0;
    threads = [None] * len(hosts)
    for host in hosts:
        threads[counter] = Thread(target = execute, args = (counter, hosts[host]["host"], hosts[host]["port"], ))
        threads[counter].start()

        counter += 1

    # Wait for all threads to finish
    for thread in threads:
        thread.join()

if __name__ == "__main__":
    if sys.argv[1] == '-c':
        config()

    if sys.argv[1] == '-d':
        data()

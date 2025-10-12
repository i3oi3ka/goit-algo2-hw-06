import json
from datetime import datetime
from datasketch import HyperLogLog

hll = HyperLogLog(p=14)


def unique_ip_address(path):
    remote_addrs = []
    with open(path, "rb") as file:
        for line in file:
            line = line.strip()
            if line:
                try:
                    log_entry = json.loads(line)
                    remote_address = log_entry.get("remote_addr")
                    if remote_address:
                        remote_addrs.append(remote_address)

                except json.JSONDecodeError:
                    print(f"Skipping malformed JSON line: {line[:60]}...")
    return remote_addrs


remote_ip_address = unique_ip_address("lms-stage-access.log")

set_ip = set()
time_start = datetime.now().second
for data in remote_ip_address:
    set_ip.add(data)
time_result = datetime.now().second - time_start


print(f"Реальна кількість унікальних елементів: {len(set_ip)}, time: {time_result}")
time_start = datetime.now()
for data in remote_ip_address:
    hll.update(data.encode("utf-8"))
time_result = datetime.now() - time_start
# Оцінка кількості унікальних елементів

print(f"Оцінена кількість унікальних елементів: {hll.count()}, time: {time_result}")

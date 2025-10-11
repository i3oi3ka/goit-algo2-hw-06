import json
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


for data in remote_ip_address:
    hll.update(data.encode("utf-8"))

# Оцінка кількості унікальних елементів
print(f"Реальна кількість унікальних елементів: {len(set(remote_ip_address))}")
print(f"Оцінена кількість унікальних елементів: {hll.count()}")

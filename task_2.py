import json


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
    return set(remote_addrs)


remote_ip_address = unique_ip_address("lms-stage-access.log")
print(remote_ip_address)

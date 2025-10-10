import json


remote_addrs = []
with open("lms-stage-access.log", "rb") as file:
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


print(remote_addrs[125])

import json


remote_addrs = []
with open("lms-stage-access.log", "rb") as file:
    for line in file:
        line = line.strip()
        if line:
            try:
                # 2. Parse the JSON string into a Python dictionary
                log_entry = json.loads(line)

                # 3. Extract the 'remote_addr' field
                remote_address = log_entry.get("remote_addr")

                if remote_address:
                    remote_addrs.append(remote_address)

            except json.JSONDecodeError:
                print(f"Skipping malformed JSON line: {line[:60]}...")


print(remote_addrs[125])

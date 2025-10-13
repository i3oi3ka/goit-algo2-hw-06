import json
import time
from datasketch import HyperLogLog


LOG_FILE = "lms-stage-access.log"


def count_unique_ip_address_set(path: str) -> int | None:
    unique_ip = set()
    try:
        with open(path, "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                if line:
                    try:
                        log_entry = json.loads(line)
                        remote_address = log_entry.get("remote_addr")
                        if remote_address:
                            unique_ip.add(remote_address)
                    except json.JSONDecodeError:
                        pass

    except FileNotFoundError:
        print(f"Error: The file at {path} was not found.")
        return None

    return len(unique_ip)


def count_unique_ip_address_hyper_log(path: str) -> int | None:
    hll = HyperLogLog(p=14)
    try:
        with open(path, "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                if line:
                    try:
                        log_entry = json.loads(line)
                        remote_address = log_entry.get("remote_addr")
                        if remote_address:
                            hll.update(remote_address.encode("utf-8"))
                    except json.JSONDecodeError:
                        pass

    except FileNotFoundError:
        print(f"Error: The file at {path} was not found.")
        return None

    return int(hll.count())


# --- Method 1: Exact counting with a set ---
time_start = time.perf_counter()
exact_count = count_unique_ip_address_set(LOG_FILE)
set_duration = time.perf_counter() - time_start


# --- Method 2: Estimated counting with HyperLogLog ---
time_start = time.perf_counter()
hll_count = count_unique_ip_address_hyper_log(LOG_FILE)
hll_duration = time.perf_counter() - time_start

error = (abs(exact_count - hll_count) / exact_count) * 100 if exact_count > 0 else 0

print("\n--- Результати порівняння ---")
print(f"| {'Метрика':<25} | {'Точний підрахунок (Set)':<25} | {'HyperLogLog':<25} |")
print(f"|{'-'*27}|{'-'*27}|{'-'*27}|")
print(f"| {'Кількість унікальних IP':<25} | {exact_count:<25} | {hll_count:<25} |")
print(
    f"| {'Час виконання (сек)':<25} | {set_duration:<25.6f} | {hll_duration:<25.6f} |"
)
print(f"| {'Похибка (%)':<25} | {'0.00 %':<25} | {f'{error:.2f} %':<25} |")
print("-" * 85)

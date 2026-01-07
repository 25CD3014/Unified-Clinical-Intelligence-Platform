from datetime import datetime
import os

def log_activity(message):
    log_path = r"d:\NEST 2.0\activity_log.txt"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(log_path, "a") as f:
        f.write(f"\n## [{timestamp}] {message}\n")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        log_activity(" ".join(sys.argv[1:]))

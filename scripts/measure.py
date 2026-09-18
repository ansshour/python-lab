"""Run a command, preserving its exit status, log and elapsed time."""
from pathlib import Path
import csv
import os
import subprocess
import sys
import time

label, *command = sys.argv[1:]
folder = Path("report/evidence")
folder.mkdir(parents=True, exist_ok=True)
start = time.perf_counter()
result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
elapsed = time.perf_counter() - start
print(result.stdout, end="")
(folder / f"{label}.log").write_text(result.stdout)
path = folder / "timings.csv"
new = not path.exists()
with path.open("a", newline="") as stream:
    writer = csv.writer(stream)
    if new:
        writer.writerow(["label", "seconds", "exit_code", "environment"])
    writer.writerow([label, f"{elapsed:.3f}", result.returncode, os.environ.get("GITHUB_ACTIONS", "local")])
sys.exit(result.returncode)

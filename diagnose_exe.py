import subprocess
import time
import httpx
from pathlib import Path

exe_path = Path("dist/Nugi Content Factory/Nugi Content Factory.exe").resolve()
print(f"Testing exe at: {exe_path}")

proc = subprocess.Popen(
    [str(exe_path)],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True
)

time.sleep(3)

print("Polling ports...")
found = False
for port in range(8000, 8010):
    try:
        r = httpx.get(f"http://127.0.0.1:{port}/api/v1/health", timeout=1.0)
        print(f"Port {port}: {r.status_code} - {r.text}")
        found = True
    except Exception as e:
        # print(f"Port {port}: {e}")
        pass

if not found:
    print("Server not responding on any port 8000-8009!")

# Check if process is still alive
ret = proc.poll()
print(f"Process poll status: {ret}")

proc.terminate()
stdout, stderr = proc.communicate(timeout=5)
print(f"STDOUT:\n{stdout}")
print(f"STDERR:\n{stderr}")

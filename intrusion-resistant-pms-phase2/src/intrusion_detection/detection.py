from datetime import datetime
import psutil
import time

# ---------- Threshold Settings ----------
CPU_THRESHOLD = 50.0        # CPU % usage considered suspicious
PROCESS_LIMIT = 150         # If system has too many active processes
SCAN_INTERVAL = 5           # Check every 5 seconds
LOG_FILE = "intrusion_logs.txt"

# ---------- Function to Log Events ----------
def log_event(event_type, pid, name, user, details):
    with open(LOG_FILE, "a") as f:
        f.write(f"{datetime.now()} | {event_type} | PID={pid} | {name} | {user} | {details}\n")
    print(f"[ALERT] {event_type}: {name} (PID={pid}) - {details}")

# ---------- Function to Check for Suspicious Processes ----------
def check_intrusion_alerts():
    alerts = []
    try:
        all_procs = list(psutil.process_iter(['pid', 'name', 'username', 'cpu_percent']))
        if len(all_procs) > PROCESS_LIMIT:
            alerts.append({'time': str(datetime.now()), 'type': 'FORK_BOMB_SUSPECT', 'details': f"Too many processes: {len(all_procs)}"})
        for proc in all_procs:
            try:
                cpu = proc.info.get('cpu_percent', 0)
                name = proc.info.get('name', '')
                user = proc.info.get('username', '')
                if cpu and cpu > CPU_THRESHOLD:
                    alerts.append({'time': str(datetime.now()), 'type': 'CPU_HOG', 'pid': proc.pid, 'name': name, 'user': user, 'cpu': cpu})
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
    except Exception as e:
        alerts.append({'time': str(datetime.now()), 'type': 'ERROR', 'details': str(e)})
    return alerts

# ---------- CLI continuous detection (keep for separate use) ----------
def detect_intrusions():
    print("\n🔍 Intrusion Detection System Running...\n")
    while True:
        try:
            alerts = check_intrusion_alerts()
            for a in alerts:
                log_event(a.get('type','ALERT'), a.get('pid','-'), a.get('name','-'), a.get('user','-'), str(a))
            time.sleep(SCAN_INTERVAL)
        except KeyboardInterrupt:
            print("\n🛑 IDS Stopped by user.")
            break
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(3)

if __name__ == "__main__":
    detect_intrusions()


import os
import subprocess
import time

def safe_fork_bomb(max_children=10):
    print("Starting safe fork bomb simulation...")
    children = []
    for _ in range(max_children):
        pid = os.fork()
        if pid == 0:
            time.sleep(10)  # child lives for 10 seconds
            exit(0)
        else:
            children.append(pid)
        time.sleep(0.5)  # slow down for safety
    for pid in children:
        os.waitpid(pid, 0)

def windows_process_bomb(max_children=10):
    print("Starting safe process bomb simulation on Windows...")
    children = []
    for _ in range(max_children):
        # Launch a harmless child process (e.g., 'timeout' command)
        p = subprocess.Popen(["timeout", "/T", "10"], shell=True)
        children.append(p)
        time.sleep(0.5)  # slow down for safety
    for p in children:
        p.wait()

if __name__ == "__main__":
    if os.name == 'posix':
        safe_fork_bomb()
    else:
        windows_process_bomb()

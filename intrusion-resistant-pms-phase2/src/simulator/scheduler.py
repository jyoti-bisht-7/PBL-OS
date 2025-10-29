import random
class Process:
    def __init__(self, pid, priority, arrival_time, burst_time):
        self.pid = pid
        self.priority = priority
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.remaining_time = burst_time
        self.cpu_usage = 0
        self.memory_consumption = 0

class Scheduler:
    def __init__(self):
        self.processes = []

    def add_process(self, process):
        self.processes.append(process)

    def round_robin(self, time_quantum):
        queue = self.processes.copy()
        time = 0
        while queue:
            process = queue.pop(0)
            if process.remaining_time > time_quantum:
                time += time_quantum
                process.remaining_time -= time_quantum
                queue.append(process)
            else:
                time += process.remaining_time
                process.cpu_usage += process.burst_time
                process.remaining_time = 0

    def priority_scheduling(self):
        self.processes.sort(key=lambda x: (x.priority, x.arrival_time))
        time = 0
        for process in self.processes:
            if time < process.arrival_time:
                time = process.arrival_time
            time += process.burst_time
            process.cpu_usage += process.burst_time

    def get_processes(self):
        return self.processes

# ---------- helper for API: return list of dicts (mock or from scheduler) ----------
def get_active_processes():
    # Return mock processes for API; replace with Scheduler instance later
    names = ["idle", "bash", "cron", "myapp", "malware", "apache", "db"]
    procs = []
    for i, n in enumerate(names, start=1000):
        procs.append({
            'pid': i,
            'name': n,
            'cpu': round(random.uniform(0, 90), 1),
            'memory': round(random.uniform(1, 80), 1),
            'priority': random.choice(['Low', 'Normal', 'High']),
            'user': random.choice(['root', 'user1', 'user2', 'www-data']),
            'state': random.choice(['Ready', 'Running', 'Blocked', 'Sandbox'])
        })
    return procs
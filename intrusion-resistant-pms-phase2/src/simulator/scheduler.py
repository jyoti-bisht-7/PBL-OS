from datetime import datetime
import psutil

class Process:
    def __init__(self, pid):
        self.pid = pid
        self.process = psutil.Process(pid)
        self.cpu_usage = self.process.cpu_percent(interval=1)
        self.memory_usage = self.process.memory_percent()
        self.name = self.process.name()
        self.status = self.process.status()
        self.user = self.process.username()
        self.create_time = datetime.fromtimestamp(self.process.create_time()).strftime("%Y-%m-%d %H:%M:%S")

class Scheduler:
    def __init__(self):
        self.processes = []

    def update_processes(self):
        self.processes = [Process(pid) for pid in psutil.pids()]

    def round_robin(self, time_quantum):
        queue = self.processes.copy()
        time = 0
        while queue:
            process = queue.pop(0)
            if process.process.is_running():
                if process.cpu_usage > time_quantum:
                    time += time_quantum
                    process.cpu_usage -= time_quantum
                    queue.append(process)
                else:
                    time += process.cpu_usage
                    process.cpu_usage = 0

    def priority_scheduling(self):
        self.processes.sort(key=lambda x: (x.process.nice(), x.create_time))
        time = 0
        for process in self.processes:
            if time < process.create_time:
                time = process.create_time
            time += process.cpu_usage

    def get_processes(self):
        return [vars(proc) for proc in self.processes]

def get_active_processes():
    return [Process(pid) for pid in psutil.pids()]
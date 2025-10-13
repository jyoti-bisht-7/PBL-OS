def detect_intrusion(processes):
    suspicious_processes = []
    
    for process in processes:
        if process['cpu_usage'] > 80:  # Excessive CPU usage
            suspicious_processes.append(process)
        elif process['memory_usage'] > 80:  # Excessive memory usage
            suspicious_processes.append(process)
        elif process['creation_rate'] > 5:  # Abnormal process creation rate
            suspicious_processes.append(process)
        elif process['waiting_time'] > 30:  # Long waiting time
            suspicious_processes.append(process)

    return suspicious_processes

def flag_suspicious_activity(suspicious_processes):
    for process in suspicious_processes:
        print(f"Suspicious activity detected in process ID: {process['id']}")
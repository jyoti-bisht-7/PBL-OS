def throttle_process(process_id):
    # Logic to lower the priority of a process
    pass

def terminate_process(process_id):
    # Logic to safely terminate a process
    pass

def mitigate_threats(suspicious_processes):
    for process in suspicious_processes:
        if process['threat_level'] == 'high':
            terminate_process(process['id'])
        elif process['threat_level'] == 'medium':
            throttle_process(process['id'])
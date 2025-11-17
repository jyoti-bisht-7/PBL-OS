from datetime import datetime
import psutil
import os

# ==================== LOGGING ====================

MITIGATION_LOG = "mitigation_logs.txt"

def log_mitigation(action, pid, name, details):
    """Log mitigation actions to file"""
    try:
        with open(MITIGATION_LOG, "a") as f:
            f.write(f"{datetime.now()} | {action} | PID={pid} | {name} | {details}\n")
        print(f"[MITIGATION] {action}: {name} (PID={pid}) - {details}")
    except Exception as e:
        print(f"Error logging mitigation: {e}")

# ==================== PROCESS MITIGATION FUNCTIONS ====================

def throttle_process(process_id):
    """Lower the priority of a process to reduce its resource consumption."""
    try:
        proc = psutil.Process(process_id)
        process_name = proc.name()
        current_nice = proc.nice()
        
        # Set lower priority (higher nice value)
        new_priority = current_nice + 5
        proc.nice(new_priority)
        
        log_mitigation(
            "THROTTLE",
            process_id,
            process_name,
            f"Priority changed from {current_nice} to {new_priority}"
        )
        
        return {
            'success': True,
            'pid': process_id,
            'name': process_name,
            'old_priority': current_nice,
            'new_priority': new_priority
        }
        
    except psutil.NoSuchProcess:
        error_msg = f"Process {process_id} does not exist"
        log_mitigation("THROTTLE_FAILED", process_id, "Unknown", error_msg)
        raise
        
    except psutil.AccessDenied:
        error_msg = f"Access denied to process {process_id}"
        log_mitigation("THROTTLE_FAILED", process_id, "Unknown", error_msg)
        raise
        
    except Exception as e:
        error_msg = f"Failed to throttle process: {str(e)}"
        log_mitigation("THROTTLE_FAILED", process_id, "Unknown", error_msg)
        raise


def terminate_process(process_id):
    """Safely terminate a process."""
    try:
        proc = psutil.Process(process_id)
        process_name = proc.name()
        
        # Try graceful termination first
        proc.terminate()
        
        # Wait for process to terminate (up to 3 seconds)
        proc.wait(timeout=3)
        
        log_mitigation(
            "TERMINATE",
            process_id,
            process_name,
            "Process terminated successfully"
        )
        
        return {
            'success': True,
            'pid': process_id,
            'name': process_name,
            'terminated': True
        }
        
    except psutil.NoSuchProcess:
        error_msg = f"Process {process_id} does not exist"
        log_mitigation("TERMINATE_FAILED", process_id, "Unknown", error_msg)
        raise
        
    except psutil.AccessDenied:
        error_msg = f"Access denied to process {process_id}"
        log_mitigation("TERMINATE_FAILED", process_id, "Unknown", error_msg)
        raise
        
    except Exception as e:
        error_msg = f"Failed to terminate process: {str(e)}"
        log_mitigation("TERMINATE_FAILED", process_id, "Unknown", error_msg)
        raise


def suspend_process(process_id):
    """Suspend a process (pause execution)."""
    try:
        proc = psutil.Process(process_id)
        process_name = proc.name()
        
        proc.suspend()
        
        log_mitigation(
            "SUSPEND",
            process_id,
            process_name,
            "Process suspended successfully"
        )
        
        return {
            'success': True,
            'pid': process_id,
            'name': process_name,
            'suspended': True
        }
        
    except psutil.NoSuchProcess:
        error_msg = f"Process {process_id} does not exist"
        log_mitigation("SUSPEND_FAILED", process_id, "Unknown", error_msg)
        raise
        
    except psutil.AccessDenied:
        error_msg = f"Access denied to process {process_id}"
        log_mitigation("SUSPEND_FAILED", process_id, "Unknown", error_msg)
        raise
        
    except Exception as e:
        error_msg = f"Failed to suspend process: {str(e)}"
        log_mitigation("SUSPEND_FAILED", process_id, "Unknown", error_msg)
        raise


def resume_process(process_id):
    """Resume a suspended process."""
    try:
        proc = psutil.Process(process_id)
        process_name = proc.name()
        
        proc.resume()
        
        log_mitigation(
            "RESUME",
            process_id,
            process_name,
            "Process resumed successfully"
        )
        
        return {
            'success': True,
            'pid': process_id,
            'name': process_name,
            'resumed': True
        }
        
    except psutil.NoSuchProcess:
        error_msg = f"Process {process_id} does not exist"
        log_mitigation("RESUME_FAILED", process_id, "Unknown", error_msg)
        raise
        
    except psutil.AccessDenied:
        error_msg = f"Access denied to process {process_id}"
        log_mitigation("RESUME_FAILED", process_id, "Unknown", error_msg)
        raise
        
    except Exception as e:
        error_msg = f"Failed to resume process: {str(e)}"
        log_mitigation("RESUME_FAILED", process_id, "Unknown", error_msg)
        raise


def set_cpu_affinity(process_id, cpu_cores):
    """Set CPU affinity for a process (limit which CPU cores it can use)."""
    try:
        proc = psutil.Process(process_id)
        process_name = proc.name()
        
        proc.cpu_affinity(cpu_cores)
        
        log_mitigation(
            "SET_CPU_AFFINITY",
            process_id,
            process_name,
            f"CPU affinity set to {cpu_cores}"
        )
        
        return {
            'success': True,
            'pid': process_id,
            'name': process_name,
            'cpu_affinity': cpu_cores
        }
        
    except psutil.NoSuchProcess:
        error_msg = f"Process {process_id} does not exist"
        log_mitigation("SET_CPU_AFFINITY_FAILED", process_id, "Unknown", error_msg)
        raise
        
    except psutil.AccessDenied:
        error_msg = f"Access denied to process {process_id}"
        log_mitigation("SET_CPU_AFFINITY_FAILED", process_id, "Unknown", error_msg)
        raise
        
    except Exception as e:
        error_msg = f"Failed to set CPU affinity: {str(e)}"
        log_mitigation("SET_CPU_AFFINITY_FAILED", process_id, "Unknown", error_msg)
        raise


# ==================== AUTOMATED MITIGATION ====================

def mitigate_threats(suspicious_processes):
    """Automatically mitigate threats based on threat level."""
    results = []
    
    for process in suspicious_processes:
        if process['cpu'] > 80:  # Example threshold
            result = throttle_process(process['pid'])
            results.append(result)
    
    return results


def auto_mitigate_high_usage(cpu_threshold=80, memory_threshold=80):
    """Automatically mitigate processes exceeding resource thresholds."""
    results = []
    
    try:
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
            if proc.info['cpu_percent'] > cpu_threshold or proc.info['memory_percent'] > memory_threshold:
                result = terminate_process(proc.info['pid'])
                results.append(result)
                
    except Exception as e:
        print(f"Error during auto mitigation: {str(e)}")
    
    return results

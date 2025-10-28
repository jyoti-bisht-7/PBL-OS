import os
from ctypes import CDLL, POINTER, c_int, c_char_p, c_void_p

_here = os.path.dirname(__file__)
lib_path = os.path.normpath(os.path.join(_here, '..', 'core', 'libcore.so'))

_lib = None
if os.path.exists(lib_path):
    try:
        _lib = CDLL(lib_path)
        # priority selection
        _lib.schedule_next_priority.argtypes = (POINTER(c_int), POINTER(c_int), POINTER(c_int), c_int)
        _lib.schedule_next_priority.restype = c_int

        # round-robin index selection
        _lib.schedule_next_rr_index.argtypes = (POINTER(c_int), POINTER(c_int), c_int, c_int)
        _lib.schedule_next_rr_index.restype = c_int

        # aging helper
        _lib.apply_aging.argtypes = (POINTER(c_int), POINTER(c_int), c_int, c_int, POINTER(c_int))
        _lib.apply_aging.restype = None

        # detection
        _lib.detect_intrusion_by_usage.argtypes = (POINTER(c_int), POINTER(c_int), POINTER(c_int), c_int, c_int, c_int, POINTER(c_int))
        _lib.detect_intrusion_by_usage.restype = c_int

        # process manager
        _lib.pm_fork_exec.argtypes = (c_char_p, POINTER(c_char_p))
        _lib.pm_fork_exec.restype = c_int

        _lib.pm_kill.argtypes = (c_int, c_int)
        _lib.pm_kill.restype = c_int
    except OSError:
        _lib = None


def _as_c_int_array(py_list):
    n = len(py_list)
    return (c_int * n)(*py_list), n


def schedule_next_priority(pids, priorities, remaining):
    """Return selected pid (or -1)."""
    if not pids:
        return -1
    PIDS, n = _as_c_int_array(pids)
    PR, _ = _as_c_int_array(priorities)
    REM, _ = _as_c_int_array(remaining)
    if _lib:
        return _lib.schedule_next_priority(PIDS, PR, REM, n)
    # fallback
    best_idx = -1
    best_prio = 10**9
    for i in range(n):
        if remaining[i] <= 0:
            continue
        if priorities[i] < best_prio:
            best_prio = priorities[i]
            best_idx = i
    return pids[best_idx] if best_idx >= 0 else -1


def schedule_next_rr_index(pids, remaining, last_index):
    """Return next index in array, or -1."""
    if not pids:
        return -1
    PIDS, n = _as_c_int_array(pids)
    REM, _ = _as_c_int_array(remaining)
    if _lib:
        return _lib.schedule_next_rr_index(PIDS, REM, n, int(last_index))
    # fallback
    start = (last_index + 1) % n if n > 0 else 0
    for i in range(n):
        idx = (start + i) % n
        if remaining[idx] > 0:
            return idx
    return -1


def apply_aging(priorities, waiting_time, aging_factor=1):
    """Return new priorities list after aging."""
    if not priorities:
        return []
    P, n = _as_c_int_array(priorities)
    W, _ = _as_c_int_array(waiting_time)
    OUT = (c_int * n)()
    if _lib:
        _lib.apply_aging(P, W, n, int(aging_factor), OUT)
        return [int(OUT[i]) for i in range(n)]
    # fallback
    out = []
    for i in range(n):
        aged = priorities[i] - (waiting_time[i] // (aging_factor if aging_factor > 0 else 1))
        out.append(max(0, aged))
    return out


def detect_intrusion_by_usage(pids, cpu, mem, cpu_threshold=80, mem_threshold=80):
    """Return (flags_list, count) where flags_list is booleans per pid."""
    if not pids:
        return [], 0
    P, n = _as_c_int_array(pids)
    CPU, _ = _as_c_int_array(cpu)
    MEM, _ = _as_c_int_array(mem)
    OUT = (c_int * n)()
    if _lib:
        cnt = _lib.detect_intrusion_by_usage(P, CPU, MEM, n, int(cpu_threshold), int(mem_threshold), OUT)
        return [bool(OUT[i]) for i in range(n)], int(cnt)
    out = []
    cnt = 0
    for i in range(n):
        flag = int(cpu[i] > cpu_threshold or mem[i] > mem_threshold)
        out.append(bool(flag))
        cnt += flag
    return out, cnt


def pm_fork_exec(path, argv):
    """Spawn a child to exec path with argv (list of bytes/str). Returns child pid or -1."""
    if _lib:
        # prepare argv as c_char_p array
        arr = (c_char_p * (len(argv) + 1))()
        for i, a in enumerate(argv):
            if isinstance(a, str):
                a = a.encode()
            arr[i] = a
        arr[len(argv)] = None
        return int(_lib.pm_fork_exec(path.encode() if isinstance(path, str) else path, arr))
    # fallback: use subprocess
    import subprocess
    try:
        p = subprocess.Popen([path] + [a.decode() if isinstance(a, bytes) else a for a in argv])
        return p.pid
    except Exception:
        return -1


def pm_kill(pid, sig=9):
    if _lib:
        return _lib.pm_kill(int(pid), int(sig)) == 0
    try:
        import os, signal
        os.kill(int(pid), int(sig))
        return True
    except Exception:
        return False

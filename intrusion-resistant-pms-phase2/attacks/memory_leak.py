import time

def memory_leak():
    print("Starting memory leak simulation (safe mode)...")
    leaky = []
    for _ in range(30):  # 30 iterations, ~30 seconds
        leaky.append(bytearray(5 * 1024 * 1024))  # allocate 5MB
        time.sleep(1)
    print("Memory leak simulation complete.")

if __name__ == "__main__":
    memory_leak()

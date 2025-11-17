
import sys
print("Attack script running with Python:", sys.executable)

import time

def cpu_hog():
    print("Starting intensified CPU hog attack...")
    end_time = time.time() + 300  # run for 5 minutes
    while time.time() < end_time:
        # Use a much larger range and more complex calculation
        [x**3 for x in range(1000000)]  # more intensive busy loop

if __name__ == "__main__":
    cpu_hog()

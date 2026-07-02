import threading
import time

# Simulates attendance processing task
def attendance_processing():
    for i in range(1, 6):
        print(f"[Attendance] Processing intern {i}")
        time.sleep(1)


# Simulates certificate generation task
def certificate_generation():
    for name in ["ABC", "PQR", "XYZ", "JHON", "BOB"]:
        print(f"[Certificate] Generated for {name}")
        time.sleep(1.5)


# Creating threads for parallel execution
t1 = threading.Thread(target=attendance_processing)
t2 = threading.Thread(target=certificate_generation)

t1.start()
t2.start()

# Waiting for both threads to finish
t1.join()
t2.join()

print("Both tasks completed successfully.")
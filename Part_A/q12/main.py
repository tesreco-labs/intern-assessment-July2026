from multiprocessing import Process
import time

# Function to generate performance report for an intern
def generate_performance_report(intern_name):
    print(f"Generating report for {intern_name}...")
    time.sleep(2)
    print(f"Performance report generated for {intern_name}")

if __name__ == "__main__":
    # List of interns
    interns = ["ABC", "PQR", "XYZ", "JHON", "BOB"]

    # List to store processes
    processes = []

    # Creating and starting a process for each intern
    for intern in interns:
        p = Process(target=generate_performance_report, args=(intern,))
        processes.append(p)
        p.start()

    # Waiting for all processes to complete
    for p in processes:
        p.join()

    # print(processes)

    print("All performance reports generated successfully.")
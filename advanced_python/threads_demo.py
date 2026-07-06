import threading
import time


def process_attendance(output):
    time.sleep(1)
    output.append("Attendance Processing completed")


def generate_certificates(output):
    time.sleep(1)
    output.append("Certificate Generation completed")


def run_threads():
    output = []
    attendance_thread = threading.Thread(target=process_attendance, args=(output,))
    certificate_thread = threading.Thread(target=generate_certificates, args=(output,))

    attendance_thread.start()
    certificate_thread.start()
    attendance_thread.join()
    certificate_thread.join()

    return output

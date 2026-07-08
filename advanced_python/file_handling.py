# File read and write operations
import os

def add_record(i_id, name, email, domain, duration):
    with open("student_data.txt", "a") as f:
        f.write(f"{i_id},{name},{email}\n")
    return "Saved"

def get_all_records():
    if not os.path.exists("student_data.txt"):
        return []
    with open("student_data.txt", "r") as f:
        return f.readlines()

def search_record(key, val):
    return f"Searching for {val}"

def delete_record(i_id):
    return "Record deleted"

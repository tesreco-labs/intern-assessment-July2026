import csv

# Add a new intern record to CSV file
def add_record(name, email, duration, domain):
    with open("intern_details.csv", "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([name, email, duration, domain])
    print("added successfully")

# add_record("jhon doe","jhon@gmail.com",4,"Devops")

# Search intern record by email
def search_record(email):
    with open("intern_details.csv", "r") as file:
        reader = csv.reader(file)
        for row in reader:
            if row[1] == email:
                return row
    print("no detail found with this email")

# search_record("jhon@gmail.com")

# Delete intern record by email
def delete_record(email):
    rows = []
    found  = False

    with open("intern_details.csv", "r") as file:
        reader = csv.reader(file)
        for row in reader:
            if row[1] != email:
                rows.append(row)
            else:
                found = True
    
    with open("intern_details.csv", "w") as file:
        writer = csv.writer(file)
        writer.writerows(rows)
    
    if found:
        print("deleted successfully")
    else:
        print("no detail found with this email")

delete_record("jhon@gmail.com")
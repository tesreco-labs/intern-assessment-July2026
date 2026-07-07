import csv
    
def store_details(intern):
    with open('interns.csv', 'a', newline='') as csvFile:
        data = csv.writer(csvFile)
        data.writerow([intern['intern_id'], intern['name'], intern['email'], intern['domain'], intern['duration']])   

def get_details(id):
    with open('interns.csv', newline='') as csvFile:
        data = csv.reader(csvFile)
        for row in data:
            if id==row[0]: print(row)

def remove(id):
    with open('interns.csv', newline='') as csvFile:
        data = csv.reader(csvFile)
        rows_after_removal = [row for row in data if row[0] != id]

    with open('interns.csv', 'w', newline='') as csvFile:
        data = csv.writer(csvFile)
        data.writerows(rows_after_removal)

intern1 = {"intern_id": "TES001", "name": "khushi", "email": "kb@gmail.com", "domain": "ML", "duration": "4 weeks"}
intern2 = {"intern_id": "TES002", "name": "kay", "email": "kay@gmail.com", "domain": "Web dev", "duration": "4 weeks"}

store_details(intern1)
store_details(intern2)

get_details("TES001")

remove("TES001")


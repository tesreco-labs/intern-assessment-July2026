# TESRECO Intern Management Portal

This project is prepared for the TESRECO Python and Flask Technical Assessment. It includes the required Advanced Python programs, Flask web pages, REST APIs, SQLite database handling, logging, and a Postman collection.

## How to Run

Install the dependency:

```bash
python -m pip install -r requirements.txt
```

Start the Flask app:

```bash
python app.py
```

Open the application:

```text
http://127.0.0.1:5000/
```

Run the Advanced Python demo:

```bash
python -B -m advanced_python.main
```

## Web Pages

```text
/                          Home page
/about                     About TESRECO
/add-intern                Add intern page
/view-interns              View interns page
/edit-intern/<intern_id>   Edit intern page
/delete-intern/<intern_id> Delete intern page
```

## APIs

```text
POST   /register
GET    /interns
PUT    /intern/<intern_id>
DELETE /intern/<intern_id>
POST   /attendance
POST   /assign-mentor
```

## Advanced Python Coverage

- Intern class with constructor, getters, setters, and __str__
- Performance calculator with decorator logging
- Custom iterator for TES intern IDs
- Generator for certificate messages
- Custom exceptions and intern validation
- Shallow copy and deep copy demonstration
- Multiple inheritance and MRO display
- Abstract Report class with attendance and performance reports
- map, filter, and reduce analysis
- CSV add, search, and delete operations
- Multithreading demo
- Multiprocessing demo
- Logging in tesreco.log
- SQLite CRUD for Interns and Mentors

## Project Structure

```text
tesreco_intern_portal/
|-- advanced_python/
|-- data/
|-- postman/
|-- static/
|   |-- css/
|   `-- images/
|-- templates/
|   `-- interns/
|-- app.py
|-- interns.db
|-- tesreco.log
|-- requirements.txt
`-- README.md
```

## Submission Files

- Complete source code
- interns.db
- postman/TESRECO_Intern_Management.postman_collection.json
- README.md
- GitHub repository link

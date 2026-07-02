import sqlite3

# Connecting to SQLite database
connection=sqlite3.connect('tesreco.db')

# Creating cursor object to execute SQL queries
cursor=connection.cursor()

# Creating Interns table if it does not exist
cursor.execute('''
Create Table If Not Exists Interns(
    intern_id Text Primary Key,
    name Text Not Null,
    email Text Not Null,
    domain Text
    )
''')

# Creating Mentors table if it does not exist
cursor.execute('''
Create Table If Not Exists Mentors(
    mentor_id Text Primary Key,
    name Text Not Null,
    specialization Text Not Null
    )
''')


connection.commit()

# Inserting record into Interns table
cursor.execute('''
Insert into Interns values('TES1','ABC','abc@gmail.com','Web Developer')
''')

# Inserting record into Mentors table
cursor.execute('''
Insert into Mentors values('MNT1','Jhon','AI/ML')
''')

connection.commit()

# Fetching all Interns records
cursor.execute('Select * from Interns')

rows = cursor.fetchall()
print(rows)

# Updating intern domain
cursor.execute('''
UPDATE Interns
Set domain='AI'
where name="ABC"
''')

connection.commit()

cursor.execute('Select * from Interns')

rows = cursor.fetchall()
print(rows)

# Deleting intern record
cursor.execute('''
Delete from Interns
where name ='ABC'
''')

connection.commit()

# Fetching final Interns records
cursor.execute('Select * from Interns')

rows = cursor.fetchall()
print(rows)

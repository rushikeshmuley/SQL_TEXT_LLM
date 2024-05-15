import sqlite3

# Connect to sqlite
connection=sqlite3.connect('student.db')

## Create a Cursor object to insert record,create,table,retrieve
cursor=connection.cursor()

## Create the table
table_info= """
CREATE TABLE STUDENT(NAME VARCHAR(25),CLASS VARCHAR(25),
SECTION VARCHAR(25),MARKS INT);
"""
cursor.execute(table_info)

# Insert Some More Records

## Insert Some more records

cursor.execute('''Insert Into STUDENT values('Krish','Data Science','A',90)''')
cursor.execute('''Insert Into STUDENT values('Sudhanshu','Data Science','B',100)''')
cursor.execute('''Insert Into STUDENT values('Darius','Data Science','A',86)''')
cursor.execute('''Insert Into STUDENT values('Vikash','DEVOPS','A',50)''')
cursor.execute('''Insert Into STUDENT values('Dipesh','DEVOPS','A',35)''')

## Display all the records
print("The inserted records are")

data=cursor.execute('''Select * from student''')

for row in data:
    print(row)

## close to sqlite

connection.commit()
connection.close
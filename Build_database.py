import psycopg2
import env
import csv
DATABASE = env.DATABASE
USER = env.USER 
PASSWORD = env.PASSWORD
HOST = env.HOST
PORT = env.PORT

# this con will establish a connection to the postgresSQL
con = psycopg2.connect(database=DATABASE, user=USER, password=PASSWORD, host=HOST, port=PORT)
print("Database opened successfully")

#cur is a cursor method that linked to the connection 
# This allows you to manage the Postgres database   
cur = con.cursor()

# execute is a method to send a SQL query to the DB
# DROP is a command that drops the specified table from the DB if it already exists. 
# WARNING: You will lose your table and its content!!!

cur.execute("DROP TABLE IF EXISTS CT_PATIENT")

# CREATE TABLE in a query to create a table in database
cur.execute('''CREATE TABLE CT_PATIENT
      (PATIENT_ID          INT PRIMARY KEY     NOT NULL,
      FIRST_NAME           TEXT    NOT NULL,
      LAST_NAME            TEXT    NOT NULL,
      AGE                  TEXT    NOT NULL,
      GENDER               TEXT    NOT NULL,
      CT_IMAGE             TEXT    NOT NULL,
      USER_ID              TEXT    NOT NULL);''')

# commit is the method in a connection that stores changes that applied by cursor 
con.commit()
print(" PATIENT table created successfully")

"""
patient_list = [
  ["00","Thomas", "Porter", "60", "M", "ID_0000_AGE_0060_CONTRAST_1_CT.dcm", "TP00"],
  ["01", "Spencer", "Arce", "69", "F", "ID_0001_AGE_0069_CONTRAST_1_CT.dcm", "SA01"],
]

for row in patient_list:
    cur.execute("INSERT INTO CT_PATIENT (PATIENT_ID,FIRST_NAME,LAST_NAME,AGE,GENDER,CT_IMAGE,USER_ID) VALUES ('%s', '%s','%s','%s','%s','%s','%s')"%(row[0],row[1],row[2],row[3],row[4],row[5],row[6]))
"""   
    
with open(r'C:\Users\USER\MDPH612 Project\Patient_data.txt', newline = '',encoding="utf-16") as file:                                                                                          
    	patient_list = csv.reader(file, delimiter='\t')
    	for row in patient_list:
            cur.execute("INSERT INTO CT_PATIENT (PATIENT_ID,FIRST_NAME,LAST_NAME,AGE,GENDER,CT_IMAGE,USER_ID) VALUES ('%s', '%s','%s','%s','%s','%s','%s')"%(row[0],row[1],row[2],row[3],row[4],row[5],row[6]))

# INSERT INTO is a query to add row to a table
# we will add patient data row by row using the for loop with string formatting

con.commit()

print(" PATIENT info successfully added!")

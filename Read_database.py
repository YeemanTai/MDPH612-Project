import psycopg2
import env
DATABASE = env.DATABASE
USER = env.USER 
PASSWORD = env.PASSWORD
HOST = env.HOST
PORT = env.PORT

def read_db(cur, table):
    # SELECT is a SQL query to read columns from a DB table.
    # * will collect all the columns
    # fetchall will return collected data
    cur.execute('SELECT * FROM %s'%table)
    rows = cur.fetchall()
    for row in rows:
        print (row)

def main():
    con = psycopg2.connect(database=DATABASE, user=USER, password=PASSWORD, host=HOST, port=PORT)
    print("Database opened successfully")
    cur = con.cursor()
    # following function is to test that your database is created correctly
    read_db(cur, 'CT_PATIENT')
if __name__ == "__main__":
    main()
from flask import Flask, Response, render_template
from flask import  request, Response
import psycopg2
import os
import env

DATABASE = env.DATABASE
USER = env.USER 
PASSWORD = env.PASSWORD
HOST = env.HOST
PORT = env.PORT

app = Flask(__name__, template_folder='templates')
app.config["DEBUG"] = True

@app.route('/list', methods=['GET'])
def list():
    return render_template("list.html", 
                                        title='Patient List',
                                        column_names = [],
                                        rows=[])

@app.route('/list', methods=['POST'])
def patient_form_post():
    p_id = request.form['p_id']
    p_firstname = request.form['p_firstname']
    p_lastname = request.form['p_lastname']
    p_age = request.form['p_age']
    p_gender = request.form['p_gender']

    query = "SELECT PATIENT_ID, FIRST_NAME, LAST_NAME, AGE, GENDER FROM CT_PATIENT WHERE"

    
    
    to_filter = []

    if p_id != '':
        query += ' patient_id=%s AND'
        to_filter.append(p_id)
    if p_firstname != '':
        query += ' first_name=%s AND'
        to_filter.append(p_firstname)
    if p_lastname != '':
        query += ' last_name=%s AND'
        to_filter.append(p_lastname)
    if p_age != '':
        query += ' age=%s AND'
        to_filter.append(p_age)
    if p_gender != '':
        query += ' gender=%s AND'
        to_filter.append(p_gender)
        

    if query[-3:] == "AND":
        query = query[:-3] 
    elif query[-5:] == "WHERE":
         query = query[:-5] 
    query += ';'

    conn = psycopg2.connect(database=DATABASE, user=USER, password=PASSWORD, host=HOST, port=PORT)
    cur = conn.cursor()
    cur.execute(query, to_filter)
    colms = [desc[0] for desc in cur.description]
    results = cur.fetchall()
    print(results)
    return render_template("list.html", title='Patient List',
                                        column_names = colms,
                                        rows=results)

app.run()
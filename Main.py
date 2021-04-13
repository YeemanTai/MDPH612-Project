# -*- coding: utf-8 -*-
"""
Created on Fri Apr  2 15:32:19 2021

@author: USER
"""

from flask import Flask, Response, request, render_template, send_from_directory, jsonify, abort, redirect
import psycopg2
import os
import env
import pydicom as dicom
import matplotlib.pyplot as plt
import numpy

DATABASE = env.DATABASE
USER = env.USER 
PASSWORD = env.PASSWORD
HOST = env.HOST
PORT = env.PORT

SERVER_IP = '127.0.0.1'
SERVER_PORT = '5000'
IMAGES_URL = 'http://%s:%s/images'%(SERVER_IP,SERVER_PORT)

app = Flask(__name__, template_folder='templates')
app.config["IMAGE_FOLDER_PATH"] = './images/JPG'
app.config["DEBUG"] = True

folder_path = r"C:\Users\USER\MDPH612 Project\images\DICOM"

@app.route('/error', methods=['GET'])
def error():
    return render_template("error.html")


@app.route('/login', methods=['GET'])
def login():
    return render_template("login.html")

@app.route('/login', methods=['GET', 'POST'])
def user_identification():
    userid = request.form.get('userid')
    pw = request.form.get('pw')
    #print(userid)
    print(pw)
    
    if userid == "doctor":
        if pw == "doctor":
            return redirect('/list')
        else:
            return redirect('/error')
    
    else:
        image_query = "SELECT FIRST_NAME, LAST_NAME, CT_IMAGE FROM CT_PATIENT WHERE patient_id=%s ;"
        conn = psycopg2.connect(database=DATABASE, user=USER, password=PASSWORD, host=HOST, port=PORT)
        cur = conn.cursor()
        cur.execute(image_query,[userid])
        firstname_lastname_imagename = cur.fetchall()
        firstname_lastname_imagename = firstname_lastname_imagename[0]
        firstname = firstname_lastname_imagename[0]
        lastname = firstname_lastname_imagename[1]
        patient_name = firstname + " " + lastname
        image_name = firstname_lastname_imagename[2]

        if pw == lastname:
            if len(image_name) != 0:
                #image_name = ''.join(image_name)
                image_name = image_name.replace('.dcm', '.jpg')
                #print(image_name)
                url =  IMAGES_URL+"/"+image_name
                #print (url)
                #return redirect(url)
                return render_template('image_patient.html', url = url, userid = userid, patient_name = patient_name)
        else:
            return redirect('/error')
        
    return render_template("login.html")
    


@app.route('/list', methods=['GET'])
def list():
    return render_template("list.html", 
                                        title='Patient List',
                                        column_names = [],
                                        rows=[])

@app.route('/list', methods=['POST'])
def patient_search():
    p_id = request.form.get('p_id')
    p_firstname = request.form.get('p_firstname')
    p_lastname = request.form.get('p_lastname')
    p_age = request.form.get('p_age')
    p_gender = request.form.get('p_gender')
    
    p_id_request = request.form.get('p_id_request')
    image_query = "SELECT CT_IMAGE FROM CT_PATIENT WHERE patient_id=%s ;"

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
    #print(results)
    
    # Display patient's CT according to the input
    cur.execute(image_query,[p_id_request])
    image_name = cur.fetchall()
    
    if len(image_name) != 0:
        image_name = ''.join(image_name[0])
        # Store the pixel array of the image and send to the front end
        ds = dicom.dcmread(os.path.join(folder_path, image_name))
        pixel_array_numpy = ds.pixel_array
        #print(pixel_array_numpy)

        
        # Convert pixels values to HU
        intercept = ds.RescaleIntercept
        slope = ds.RescaleSlope
        hu_array_numpy = pixel_array_numpy * slope + intercept
        
        pixel_array_numpy = pixel_array_numpy.tolist()
        numpy.savetxt("foo.csv", hu_array_numpy, delimiter=",")
        hu_array_numpy =  hu_array_numpy.tolist()
        
        image_name = image_name.replace('.dcm', '.jpg')
        url =  IMAGES_URL+"/"+image_name


        # Display patient info on the page
        info_query = "SELECT PATIENT_ID, FIRST_NAME, LAST_NAME, AGE, GENDER FROM CT_PATIENT WHERE patient_id=%s ;"
        cur.execute(info_query, [p_id_request])
        info = cur.fetchall()
        print(info[0])
        info = info[0]
        p_id = info[0]
        p_name = info[1] + " " + info[2]
        p_age = info[3]
        p_gender = info[4]
    
        return render_template('image_doctor.html', url = url, pixel_array_numpy = pixel_array_numpy, hu_array_numpy = hu_array_numpy, p_id = p_id, p_name = p_name, p_age = p_age, p_gender = p_gender )
    
    return render_template("list.html", title='Patient List',
                                        column_names = colms,
                                        rows=results)



@app.route("/images/<image_name>/", methods=['GET', 'POST'])
def get_patient_file(image_name):
    print (app.config["IMAGE_FOLDER_PATH"], image_name) 
    try:
        return send_from_directory(app.config["IMAGE_FOLDER_PATH"], filename=image_name)
    except:
        abort(404, description="Image %s not found."%image_name)



app.run(host=SERVER_IP, port=SERVER_PORT)
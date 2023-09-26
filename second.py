from flask import Blueprint, render_template

from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from PIL import Image, ImageDraw, ImageFont, ImageOps
image = Image.new('RGB', (1200,900), (255, 255, 255))
draw = ImageDraw.Draw(image)
font = ImageFont.truetype('arial.ttf', size=45)
from time import sleep
import random
import os
import datetime
from datetime import timedelta
import pyqrcode
from flask_mysqldb import MySQL
from flask import Flask
from flask import Flask, flash, redirect, render_template, request, session, abort, url_for, g
import os

import itertools
import smtplib

app = Flask(__name__)
Bootstrap(app)

mysql = MySQL()
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'test'

mysql.init_app(app)


second = Blueprint("second",__name__, static_folder="static", template_folder="templates")




@second.route("/")
@second.route('/login.html', methods=['POST','GET'])
def login():
    
    if request.method == 'POST':
        session.permanent = True
        l_EMAil=request.form['l_EMAil']
        session["l_EMAil"] = l_EMAil
        
        password=request.form['password']
        
       # if request.form['password'] == 'password':
            #session['l_EMAil'] = request.form['l_EMAil']
            
            
        

        cur = mysql.connection.cursor()
        result=cur.execute("SELECT admin_pass FROM admin_login WHERE admin_email=%s",(l_EMAil,))
       
        
        data=cur.fetchall()
        for row in data:
            
            
            auth_pass=row[0]
            
        
        if result>0 and password==auth_pass:

            return redirect('dash.html')
        
        else:
            
            flash(" plase check your email or password ")

        #if data:
            #session['loggedin']= True
            #session['id']= data['id']
            #session['l_EMAil']= data['l_EMAil']
            #return redirect('dashboard.html')
       # else:
            #flash(" plase check your email or password ")
            
            
        
        mysql.connection.commit()
        cur.close()




        
     
    return render_template('login.html' )



@second.route("/dash.html",methods=['POST','GET'])

def dash():
     if "l_EMAil" in session:
         l_EMAil = session["l_EMAil"]
         return render_template('dash.html',l_EMAil=l_EMAil)
     else:
         return redirect('login.html')
     return render_template('dash.html') 

@second.route("/employee_A.html")
def employee_A():

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM attendance")
    data2 = cur.fetchall()


    
    return render_template("employee_A.html",data=data2)

@second.route("/admin_show_id.html")
def showid():

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM pydata")
    data2 = cur.fetchall()

    
    return render_template("admin_show_id.html",data=data2)
    


                                   





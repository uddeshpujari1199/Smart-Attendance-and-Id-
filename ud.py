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
from wtforms import Form, BooleanField, StringField, PasswordField, validators
import os
from second import second
import itertools
import smtplib
import bcrypt



app = Flask(__name__)
Bootstrap(app)
app.permanent_session_lifetime = timedelta(minutes=30)
app.register_blueprint(second, url_prefix="/admin")

mysql = MySQL()
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'test'

mysql.init_app(app)

name="uddesh"

           

@app.before_request
def before_request():
    allowed_url = ['index','signup','login']
    print(session)
    if request.endpoint not in allowed_url and 'l_EMAil' not in session:
        return redirect('/index.html')


@app.route('/index.html')
def index():
    return render_template('index.html')



@app.route('/login.html', methods=['POST','GET'])
def login():
    
    if request.method == 'POST':
        session.permanent = True
        l_EMAil=request.form['l_EMAil']
        session["l_EMAil"] = l_EMAil
        
        password=request.form['password']

        ad_pass=None
        
        cur = mysql.connection.cursor()
        result=cur.execute("SELECT admin_pass FROM admin_login WHERE admin_email=%s",(l_EMAil,))
       
        
        data1=cur.fetchall()
        for row1 in data1:

            
           
            
            ad_pass=row1[0]

        if password==ad_pass:
            return redirect('dash.html')
        
        elif ad_pass==None:

            cur = mysql.connection.cursor()
            result=cur.execute("SELECT PASS FROM register2 WHERE EMail=%s",(l_EMAil,))
           
            
            data=cur.fetchall()
            for row in data:
                
                
                auth_pass=row[0]
                
            
            if result>0 and password==auth_pass:

                return redirect('dashboard.html')
        
        else:
            
            flash(" plase check your email or password ")

        
            
            
        
        mysql.connection.commit()
        cur.close()




        
     
    return render_template('login.html' )


@app.route('/signup.html', methods=['POST','GET'])
def signup():
    if request.method == 'POST':
        
        name=request.form['name']
        email=request.form['email']
        contact=request.form['contact']
        
            
        password=request.form['password']#.encode("utf-8")
        #hashed = bcrypt.hashpw(password, bcrypt.gensalt())
        
        DOB=request.form['DOB']
        address=request.form['address']

        idno=random.randint(10000000,90000000)
        token = email+str(idno)

        

        

        
        #password validation

        if not len(password) >= 8:
            flash("password is must be 8 charecters in length")
            return redirect(request.url)

       
        
        else:
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO register2(user, EMail, PASS, contact, address, DOB) VALUES( %s, %s, %s, %s, %s, %s)",(name, email,  hashed, contact, address, DOB))
            mysql.connection.commit()
            cur.close()

            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO token(t_email, token_no) VALUES( %s, %s)",(email, token))
            mysql.connection.commit()
            cur.close()


            #sending token to user
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.ehlo()
            server.starttls()
            server.login("uddesh.pujari123@gmail.com","8898702274" )
            server.sendmail("uddesh.pujari123@gmail.com", email, token )
            
            server.close()
            flash("Account created susssefully!")
            return redirect('login.html')
   
        
    return render_template('signup.html')

#user dashboard
           
@app.route('/dashboard.html',methods=['POST','GET'])
def dashboard():
    if "l_EMAil" in session:
        l_EMAil = session["l_EMAil"]
        
        return render_template('dashboard.html',l_EMAil=l_EMAil)
    else:
        
        return redirect('login.html')

    
    
    return render_template('dashboard.html')    
    

#id_generation code

@app.route('/id_generation2.html', methods=['POST','GET'])
def idgenrat():
    if "l_EMAil" in session:
        if request.method == 'POST':
            (x, y) = (320, 50)
            company='UD ENTERPRISE'
            color = 'rgb(0, 0, 0)'
            bgcolor='rgb(0, 0, 0)'
            font = ImageFont.truetype('arial.ttf', size=50)
            draw.text((x, y), company, fill=color, font=font, bgcolor=bgcolor)


        # adding an unique id number. You can manually take it from user
            (x, y) = (50, 240)
            idno=random.randint(10000000,90000000)
            message = "Id: "+str('ID '+str(idno))
            ID=str(company)+str(idno)
            color = 'rgb(0, 0, 0)' # black color
            font = ImageFont.truetype('arial.ttf', size=35)
            draw.text((x, y), message, fill=color, font=font)

        # add pic in id
        
            profile = request.files['profo']
        
            ud=profile.save(ID+".bmp")
    
       

        # add name in id
            (x, y) = (50, 310)
            name = request.form['ID_name']
            msg="Name: "+name
            color = 'rgb(0, 0, 0)' # black color
            font = ImageFont.truetype('arial.ttf', size=30)
            draw.text((x, y), msg, fill=color, font=font)


        # add name in age
            (x, y) = (50, 380)
            age = request.form['ID_age']
            message="Age: "+age
            color = 'rgb(0, 0, 0)' # black color 
            draw.text((x, y), message, fill=color, font=font)

        # add name in dob

            (x, y) = (50, 450)
            dob = request.form['ID_DOB']
            message="Dob: "+dob
            color = 'rgb(0, 0, 0)' # black color 
            draw.text((x, y), message, fill=color, font=font)


        # add name in contact
            (x, y) = (50, 520)
            contact = request.form['ID_contact']
            message="Contact: "+contact
            color = 'rgb(0, 0, 0)' # black color 
            draw.text((x, y),message, fill=color, font=font)

        # add name in email
            (x, y) = (50, 590)
            email = request.form['ID_email']
            message="E-mail: "+email
            color = 'rgb(0, 0, 0)' # black color 
            draw.text((x, y), message, fill=color, font=font)

            cur = mysql.connection.cursor()
            cur.execute("SELECT Email2 FROM pydata")
            data = cur.fetchall()

            emailv=[]
            for row in data:
                emailv.append(row)
            emailv2=list(itertools.chain(*emailv))
            print(emailv2)

            if email in emailv2:
                flash(" your id is already created")
                return redirect("id_generation2.html")
        

            (x, y) = (50, 700)
            address = request.form['ID_address']
            message="Add: "+address
            color = 'rgb(0, 0, 0)' # black color 
            draw.text((x, y), message, fill=color, font=font)


            #token for id
            tokenv = request.form['token']

            t_v=[]

            cur = mysql.connection.cursor()
            cur.execute("SELECT t_email FROM token")
            tv = cur.fetchall()

            
            for row in tv:
                t_v.append(row)
            t_v=list(itertools.chain(*t_v))
            print(t_v)

            if email not in t_v:
                flash(" token invalid ")
                return redirect("id_generation2.html")

            
            cur = mysql.connection.cursor()
            cur.execute("SELECT token_no FROM token WHERE t_email=%s",(email,))
            data2 = cur.fetchall()

            

            for row in data2:
                token_v = row[0]

            cur = mysql.connection.cursor()
            cur.execute("DELETE FROM token WHERE t_email=%s",(email,))
            cur.close()

            

            

   




        # save the edited image
         
            image.save(str(name)+'.bmp')



            img = pyqrcode.create(str(company)+str(idno))# this info. is added in QR code, also add other things
            img.png(str(idno)+'.bmp',scale=9)


            im = Image.open(str(idno)+'.bmp')
            img_with_border = ImageOps.expand(im,border=8,fill='black') # adding border to qr code
            img_with_border.save(str(idno)+'.bmp')


            til = Image.open(name+'.bmp')
            img_with_border = ImageOps.expand(til,border=15,fill='black') # adding border to ID
            img_with_border.save(name+'.bmp')

            til = Image.open(name+'.bmp')
            im = Image.open(str(idno)+'.bmp')     # ID generation
            sym = Image.open("symbol.bmp")
            pic = Image.open(ID+".bmp")
            til.paste(sym,(50,50)) #symbol
            til.paste(pic,(880,50)) # profile
            til.paste(im,(790,340))
            til.save(name+'.bmp')
         
        
            cur = mysql.connection.cursor()
            cur.execute( "INSERT INTO pydata(ID, company, name, age, dob, contact, Email2, address, pro) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",(ID, company, name, age, dob, contact, email, address, profile))
            mysql.connection.commit()
            cur.close()

            flash("id created succesfully")
   
    return render_template("id_generation2.html")





#employee attedence

@app.route("/employee_A.html",methods=['POST','GET'])
def employee_A():

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM attendance")
    data2 = cur.fetchall()


    
    return render_template("employee_A.html",data=data2)

#employee id's

@app.route("/admin_show_id.html",methods=['POST','GET'])
def showid():

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM pydata")
    data2 = cur.fetchall()

    
    return render_template("admin_show_id.html",data=data2)

#user profile

@app.route('/pro.html',methods=['POST','GET'])
def pro():
    if "l_EMAil" in session:
        l_EMAil = session["l_EMAil"]
        
        cur = mysql.connection.cursor()
        result=cur.execute("SELECT * FROM register2 WHERE EMail=%s",(l_EMAil,))
        data=cur.fetchall()
        

    
    return render_template('pro.html',data2=data,l_EMAil=l_EMAil)

#user query

@app.route('/help.html', methods=['POST','GET'])
def help():
    if "l_EMAil" in session:
        l_EMAil = session["l_EMAil"]
        if request.method == 'POST':
            msg=request.form['help']
            cur = mysql.connection.cursor()
            cur.execute( "INSERT INTO help(help_me, help_email) VALUES (%s, %s)",( msg, l_EMAil))
            mysql.connection.commit()
            cur.close()

            flash("your query is submited successfully ")
    
    return render_template('help.html')

#admin dashboard

@app.route('/dash.html',methods=['POST','GET'])
def run():
    return render_template('dash.html')

#show query to admin

@app.route('/ad_query.html',methods=['POST','GET'])
def query():
    if "l_EMAil" in session:
        l_EMAil = session["l_EMAil"]
        
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM help")
        data2 = cur.fetchall()

    return render_template('ad_query.html',data=data2)

#delect query from admin

@app.route('/delete/<string:l_EMAil>', methods = ['GET'])
def delete(l_EMAil):
    flash("Record Has Been Deleted Successfully")
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM help WHERE help_email=%s", (l_EMAil,))
    mysql.connection.commit()
    flash("Record Has Been Deleted Successfully")
    return redirect(url_for('query'))


@app.route('/admin_pro.html',methods=['POST','GET'])
def admin_pro():
    if "l_EMAil" in session:
        l_EMAil = session["l_EMAil"]

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM admin_login")
        data2 = cur.fetchall()
        
   

    return render_template('admin_pro.html',data=data2)




    
    





if __name__ == '__main__':
    app.secret_key = os.urandom(12)
    app.run(debug=True,host='127.0.0.1', port=3000)
